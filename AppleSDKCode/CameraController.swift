/*
See the LICENSE.txt file for this sample’s licensing information.

Abstract:
An object that configures and manages the capture pipeline to stream video and LiDAR depth data.
*/

import Foundation
import AVFoundation
import CoreImage
import ImageIO
import Accelerate
import UIKit

protocol CaptureDataReceiver: AnyObject {
    func onNewData(capturedData: CameraCapturedData)
    func onNewPhotoData(capturedData: CameraCapturedData)
}

class CameraController: NSObject, ObservableObject {
    
    enum ConfigurationError: Error {
        case lidarDeviceUnavailable
        case requiredFormatUnavailable
    }
    
    private let preferredWidthResolution = 1920
    
    private let videoQueue = DispatchQueue(label: "com.example.apple-samplecode.VideoQueue", qos: .userInteractive)
    
    private(set) var captureSession: AVCaptureSession!
    
    private var photoOutput: AVCapturePhotoOutput!
    private var depthDataOutput: AVCaptureDepthDataOutput!
    private var videoDataOutput: AVCaptureVideoDataOutput!
    private var outputVideoSync: AVCaptureDataOutputSynchronizer!
    
    private var textureCache: CVMetalTextureCache!
    
    weak var delegate: CaptureDataReceiver?
    
    var isFilteringEnabled = false {
        didSet {
            depthDataOutput.isFilteringEnabled = isFilteringEnabled
        }
    }
    
    override init() {
        
        // Create a texture cache to hold sample buffer textures.
        CVMetalTextureCacheCreate(kCFAllocatorDefault,
                                  nil,
                                  MetalEnvironment.shared.metalDevice,
                                  nil,
                                  &textureCache)
        
        super.init()
        
        do {
            try setupSession()
        } catch {
            fatalError("Unable to configure the capture session.")
        }
    }
    
    private func setupSession() throws {
        captureSession = AVCaptureSession()
        captureSession.sessionPreset = .inputPriority

        // Configure the capture session.
        captureSession.beginConfiguration()
        
        try setupCaptureInput()
        setupCaptureOutputs()
        
        // Finalize the capture session configuration.
        captureSession.commitConfiguration()
    }
    
    private func setupCaptureInput() throws {
        // Look up the LiDAR camera.
        guard let device = AVCaptureDevice.default(.builtInLiDARDepthCamera, for: .video, position: .back) else {
            throw ConfigurationError.lidarDeviceUnavailable
        }
        
        // Find a match that outputs video data in the format the app's custom Metal views require.
        guard let format = (device.formats.last { format in
            format.formatDescription.dimensions.width == preferredWidthResolution &&
            format.formatDescription.mediaSubType.rawValue == kCVPixelFormatType_420YpCbCr8BiPlanarFullRange &&
            !format.isVideoBinned &&
            !format.supportedDepthDataFormats.isEmpty
        }) else {
            throw ConfigurationError.requiredFormatUnavailable
        }
        
        // Find a match that outputs depth data in the format the app's custom Metal views require.
        guard let depthFormat = (format.supportedDepthDataFormats.last { depthFormat in
            depthFormat.formatDescription.mediaSubType.rawValue == kCVPixelFormatType_DepthFloat16
        }) else {
            throw ConfigurationError.requiredFormatUnavailable
        }
        
        // Begin the device configuration.
        try device.lockForConfiguration()

        // Configure the device and depth formats.
        device.activeFormat = format
        device.activeDepthDataFormat = depthFormat

        // Finish the device configuration.
        device.unlockForConfiguration()
        
        print("Selected video format: \(device.activeFormat)")
        print("Selected depth format: \(String(describing: device.activeDepthDataFormat))")
        
        // Add a device input to the capture session.
        let deviceInput = try AVCaptureDeviceInput(device: device)
        captureSession.addInput(deviceInput)
    }
    
    private func setupCaptureOutputs() {
        // Create an object to output video sample buffers.
        videoDataOutput = AVCaptureVideoDataOutput()
        captureSession.addOutput(videoDataOutput)
        
        // Create an object to output depth data.
        depthDataOutput = AVCaptureDepthDataOutput()
        depthDataOutput.isFilteringEnabled = isFilteringEnabled
        captureSession.addOutput(depthDataOutput)

        // Create an object to synchronize the delivery of depth and video data.
        outputVideoSync = AVCaptureDataOutputSynchronizer(dataOutputs: [depthDataOutput, videoDataOutput])
        outputVideoSync.setDelegate(self, queue: videoQueue)

        // Enable camera intrinsics matrix delivery.
        guard let outputConnection = videoDataOutput.connection(with: .video) else { return }
        if outputConnection.isCameraIntrinsicMatrixDeliverySupported {
            outputConnection.isCameraIntrinsicMatrixDeliveryEnabled = true
        }
        
        // Create an object to output photos.
        photoOutput = AVCapturePhotoOutput()
        photoOutput.maxPhotoQualityPrioritization = .quality
        captureSession.addOutput(photoOutput)

        // Enable delivery of depth data after adding the output to the capture session.
        photoOutput.isDepthDataDeliveryEnabled = true
    }
    
    func startStream() {
        captureSession.startRunning()
    }
    
    func stopStream() {
        captureSession.stopRunning()
    }
}

// MARK: Output Synchronizer Delegate
extension CameraController: AVCaptureDataOutputSynchronizerDelegate {
    
    func dataOutputSynchronizer(_ synchronizer: AVCaptureDataOutputSynchronizer,
                                didOutput synchronizedDataCollection: AVCaptureSynchronizedDataCollection) {
        // Retrieve the synchronized depth and sample buffer container objects.
        guard let syncedDepthData = synchronizedDataCollection.synchronizedData(for: depthDataOutput) as? AVCaptureSynchronizedDepthData,
              let syncedVideoData = synchronizedDataCollection.synchronizedData(for: videoDataOutput) as? AVCaptureSynchronizedSampleBufferData else { return }
        
        guard let pixelBuffer = syncedVideoData.sampleBuffer.imageBuffer,
              let cameraCalibrationData = syncedDepthData.depthData.cameraCalibrationData else { return }
        
        // Package the captured data.
        let data = CameraCapturedData(depth: syncedDepthData.depthData.depthDataMap.texture(withFormat: .r16Float, planeIndex: 0, addToCache: textureCache),
                                      colorY: pixelBuffer.texture(withFormat: .r8Unorm, planeIndex: 0, addToCache: textureCache),
                                      colorCbCr: pixelBuffer.texture(withFormat: .rg8Unorm, planeIndex: 1, addToCache: textureCache),
                                      cameraIntrinsics: cameraCalibrationData.intrinsicMatrix,
                                      cameraReferenceDimensions: cameraCalibrationData.intrinsicMatrixReferenceDimensions)
        
        delegate?.onNewData(capturedData: data)
    }
}

// MARK: Photo Capture Delegate
extension CameraController: AVCapturePhotoCaptureDelegate {
    
    func capturePhoto() {
        var photoSettings: AVCapturePhotoSettings
        if  photoOutput.availablePhotoPixelFormatTypes.contains(kCVPixelFormatType_420YpCbCr8BiPlanarFullRange) {
            photoSettings = AVCapturePhotoSettings(format: [
                kCVPixelBufferPixelFormatTypeKey as String: kCVPixelFormatType_420YpCbCr8BiPlanarFullRange
            ])
        } else {
            photoSettings = AVCapturePhotoSettings()
        }
        
        // Capture depth data with this photo capture.
        photoSettings.isDepthDataDeliveryEnabled = true
        photoOutput.capturePhoto(with: photoSettings, delegate: self)
    }
    
        func photoOutput(_ output: AVCapturePhotoOutput, didFinishProcessingPhoto photo: AVCapturePhoto, error: Error?) {
            
            // Retrieve the image and depth data.
            guard let pixelBuffer = photo.pixelBuffer,
                  let depthData = photo.depthData,
                  let cameraCalibrationData = depthData.cameraCalibrationData else { return }
            
            // Stop the stream until the user returns to streaming mode.
            stopStream()
                
            // Convert the depth data to the expected format.
            let convertedDepth = depthData.converting(toDepthDataType: kCVPixelFormatType_DepthFloat16)
            
            let depthPixelBuffer = convertedDepth.depthDataMap
            
            //---intrinsic matrix
            // 📌 Intrinsische Matrix und Referenzdimensionen ausgeben
            let intrinsicMatrix = cameraCalibrationData.intrinsicMatrix
            let referenceDimensions = cameraCalibrationData.intrinsicMatrixReferenceDimensions
            
            print("📸 Intrinsische Matrix:")
            print("[ \(intrinsicMatrix.columns.0.x), \(intrinsicMatrix.columns.1.x), \(intrinsicMatrix.columns.2.x) ]")
            print("[ \(intrinsicMatrix.columns.0.y), \(intrinsicMatrix.columns.1.y), \(intrinsicMatrix.columns.2.y) ]")
            print("[ \(intrinsicMatrix.columns.0.z), \(intrinsicMatrix.columns.1.z), \(intrinsicMatrix.columns.2.z) ]")
            
            print("📏 Referenzdimensionen: Width = \(referenceDimensions.width), Height = \(referenceDimensions.height)")

            //----stop
            

            // Diren:  Debug-Check: Ist es wirklich Float16?
            let pixelFormatType = CVPixelBufferGetPixelFormatType(depthPixelBuffer)
            print("📌 PixelBuffer Format nach Konvertierung: \(pixelFormatType)")

            //Diren: Extrahieren der Tiefenwerte als Array
            let depthValues = extractDepthData(from: depthPixelBuffer)
            print("🔍 Erste Tiefenwerte (sollten Float sein):", depthValues.prefix(10))

            // Diren: Bildgröße ermitteln
                let width = CVPixelBufferGetWidth(depthPixelBuffer)
                let height = CVPixelBufferGetHeight(depthPixelBuffer)

            // Diren: Speichere die Daten als Binary-Datei
            saveDepthToBinary(depthValues: depthValues, width: width, height: height, fileName: "DepthMap")

            //Diren: Intrinsische Matrix extrahieren
            if let cameraCalibrationData = depthData.cameraCalibrationData {
                saveCameraIntrinsics(intrinsicMatrix: cameraCalibrationData.intrinsicMatrix, fileName: "camera_intrinsics")
            }

            //Diren: Farbbild für RGBD-Bild extrahieren
            if let imageData = photo.fileDataRepresentation(),
               let image = UIImage(data: imageData) {
                saveColorImage(image: image, fileName: "color_image")
            }

            
            // Package the captured data.
            let data = CameraCapturedData(depth: convertedDepth.depthDataMap.texture(withFormat: .r16Float, planeIndex: 0, addToCache: textureCache),
                                          colorY: pixelBuffer.texture(withFormat: .r8Unorm, planeIndex: 0, addToCache: textureCache),
                                          colorCbCr: pixelBuffer.texture(withFormat: .rg8Unorm, planeIndex: 1, addToCache: textureCache),
                                          cameraIntrinsics: cameraCalibrationData.intrinsicMatrix,
                                          cameraReferenceDimensions: cameraCalibrationData.intrinsicMatrixReferenceDimensions)
            
            delegate?.onNewPhotoData(capturedData: data)
        }


        func extractDepthData(from pixelBuffer: CVPixelBuffer) -> [Float16] {
            CVPixelBufferLockBaseAddress(pixelBuffer, .readOnly)
            defer { CVPixelBufferUnlockBaseAddress(pixelBuffer, .readOnly) }

            guard let baseAddress = CVPixelBufferGetBaseAddress(pixelBuffer) else {
                print("❌ Fehler: Kann Base Address nicht abrufen.")
                return []
            }

            let width = CVPixelBufferGetWidth(pixelBuffer)
            let height = CVPixelBufferGetHeight(pixelBuffer)
            let count = width * height

            // Float16 Buffer auslesen
            let bufferPointer = baseAddress.assumingMemoryBound(to: Float16.self)
            let depthData = Array(UnsafeBufferPointer(start: bufferPointer, count: count))
            
            print("Width: \(width), Height: \(height), Count: \(count)")
            
            return depthData
        }

    func saveDepthToBinary(depthValues: [Float16], width: Int, height: Int, fileName: String) {
        let fileManager = FileManager.default
        let documentsDirectory = fileManager.urls(for: .documentDirectory, in: .userDomainMask).first!
        let fileURL = documentsDirectory.appendingPathComponent("\(fileName).bin")

        do {
            // 📌 Debugging: Prüfe die ersten Werte
            print("📌 Speichere Tiefendaten...")
            print("🔍 Erste Werte vor Speicherung:", depthValues.prefix(10))

            // ✨ Speichere `width` & `height` als Float32 für einfaches Auslesen
            var metadata: [Float32] = [Float32(width), Float32(height)]
            let metadataData = Data(buffer: UnsafeBufferPointer(start: &metadata, count: metadata.count))

            // ✨ Dann die eigentlichen `Float16` Tiefendaten
            let depthData = Data(buffer: UnsafeBufferPointer(start: depthValues, count: depthValues.count))

            // ✨ Kombiniere Header (Width, Height) + Tiefendaten
            let fullData = metadataData + depthData

            // ✨ Schreibe alles in die Datei
            try fullData.write(to: fileURL)

            print("✅ Float16-Tiefendaten erfolgreich gespeichert: \(fileURL)")

        } catch {
            print("❌ Fehler beim Speichern der Datei: \(error)")
        }
    }

    func saveCameraIntrinsics(intrinsicMatrix: simd_float3x3, fileName: String) {
        let documentsDirectory = FileManager.default.urls(for: .documentDirectory, in: .userDomainMask).first!
        let fileURL = documentsDirectory.appendingPathComponent("\(fileName).json")

        // JSON-Daten erstellen
        let jsonDict: [String: Any] = [
            "fx": intrinsicMatrix[0, 0],
            "fy": intrinsicMatrix[1, 1],
            "cx": intrinsicMatrix[2, 0],
            "cy": intrinsicMatrix[2, 1]
        ]

        do {
            let jsonData = try JSONSerialization.data(withJSONObject: jsonDict, options: .prettyPrinted)
            try jsonData.write(to: fileURL)
            print("✅ Kameraintrinsics gespeichert: \(fileURL)")
        } catch {
            print("❌ Fehler beim Speichern der Kameraintrinsics: \(error)")
        }
    }


    func saveColorImage(image: UIImage, fileName: String) {
        let documentsDirectory = FileManager.default.urls(for: .documentDirectory, in: .userDomainMask).first!
        let fileURL = documentsDirectory.appendingPathComponent("\(fileName).jpg")

        if let imageData = image.jpegData(compressionQuality: 0.9) {
            do {
                try imageData.write(to: fileURL)
                print("✅ Farbbild gespeichert: \(fileURL)")
            } catch {
                print("❌ Fehler beim Speichern des Farbbilds: \(error)")
            }
        }
    }

}
