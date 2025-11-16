'use client'

import { Suspense, useRef, useState } from 'react'
import { Canvas, useLoader } from '@react-three/fiber'
import { OrbitControls, PerspectiveCamera, Grid, Environment } from '@react-three/drei'
import { STLLoader } from 'three/examples/jsm/loaders/STLLoader'
import * as THREE from 'three'

interface ModelViewerProps {
  modelUrl?: string
  modelType?: 'stl' | 'step' | 'obj'
  partName?: string
}

/**
 * 3D Model Viewer Component
 *
 * Displays CAD models (STL, STEP, OBJ) with interactive controls
 * Perfect for visual verification of parts
 */
export default function ModelViewer({ modelUrl, modelType = 'stl', partName }: ModelViewerProps) {
  const [showWireframe, setShowWireframe] = useState(false)
  const [showDimensions, setShowDimensions] = useState(true)
  const [autoRotate, setAutoRotate] = useState(false)

  if (!modelUrl) {
    return (
      <div className="bg-slate-100 rounded-lg border-2 border-dashed border-slate-300 p-8 text-center">
        <div className="text-slate-500">
          <svg className="mx-auto h-12 w-12 mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2zM9 9h6v6H9V9z" />
          </svg>
          <p className="font-medium">No 3D model available</p>
          <p className="text-sm mt-1">Upload a CAD file to view</p>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-4">
      {/* Controls */}
      <div className="flex items-center justify-between bg-slate-50 rounded-lg p-3 border border-slate-200">
        <div className="flex items-center space-x-4">
          <label className="flex items-center space-x-2">
            <input
              type="checkbox"
              checked={showWireframe}
              onChange={(e) => setShowWireframe(e.target.checked)}
              className="rounded border-slate-300"
            />
            <span className="text-sm text-slate-700">Wireframe</span>
          </label>
          <label className="flex items-center space-x-2">
            <input
              type="checkbox"
              checked={showDimensions}
              onChange={(e) => setShowDimensions(e.target.checked)}
              className="rounded border-slate-300"
            />
            <span className="text-sm text-slate-700">Dimensions</span>
          </label>
          <label className="flex items-center space-x-2">
            <input
              type="checkbox"
              checked={autoRotate}
              onChange={(e) => setAutoRotate(e.target.checked)}
              className="rounded border-slate-300"
            />
            <span className="text-sm text-slate-700">Auto-rotate</span>
          </label>
        </div>
        {partName && (
          <span className="text-sm font-medium text-slate-700">{partName}</span>
        )}
      </div>

      {/* 3D Viewer */}
      <div className="bg-slate-900 rounded-lg overflow-hidden border border-slate-700" style={{ height: '500px' }}>
        <Canvas shadows>
          <Suspense fallback={<LoadingFallback />}>
            <PerspectiveCamera makeDefault position={[30, 30, 30]} />
            <OrbitControls
              autoRotate={autoRotate}
              autoRotateSpeed={2}
              enableDamping
              dampingFactor={0.05}
            />

            {/* Lighting */}
            <ambientLight intensity={0.5} />
            <directionalLight position={[10, 10, 5]} intensity={1} castShadow />
            <directionalLight position={[-10, -10, -5]} intensity={0.3} />
            <pointLight position={[0, 10, 0]} intensity={0.5} />

            {/* Environment */}
            <Environment preset="city" />

            {/* Grid */}
            <Grid
              args={[100, 100]}
              cellSize={5}
              cellThickness={0.5}
              cellColor="#6b7280"
              sectionSize={10}
              sectionThickness={1}
              sectionColor="#9ca3af"
              fadeDistance={200}
              fadeStrength={1}
              followCamera={false}
              infiniteGrid
            />

            {/* Model */}
            <Model
              url={modelUrl}
              type={modelType}
              wireframe={showWireframe}
              showDimensions={showDimensions}
            />
          </Suspense>
        </Canvas>
      </div>

      {/* Instructions */}
      <div className="bg-blue-50 rounded-lg p-3 border border-blue-200">
        <p className="text-sm text-blue-900">
          <strong>Controls:</strong> Left-click + drag to rotate • Right-click + drag to pan • Scroll to zoom
        </p>
      </div>
    </div>
  )
}

/**
 * Model component that loads and displays 3D files
 */
function Model({ url, type, wireframe, showDimensions }: {
  url: string
  type: 'stl' | 'step' | 'obj'
  wireframe: boolean
  showDimensions: boolean
}) {
  const meshRef = useRef<THREE.Mesh>(null)

  // Load STL file
  const geometry = useLoader(STLLoader, url)

  // Center the geometry
  geometry.center()

  // Calculate bounding box for dimensions
  geometry.computeBoundingBox()
  const bbox = geometry.boundingBox!
  const dimensions = {
    x: bbox.max.x - bbox.min.x,
    y: bbox.max.y - bbox.min.y,
    z: bbox.max.z - bbox.min.z,
  }

  return (
    <group>
      <mesh
        ref={meshRef}
        geometry={geometry}
        castShadow
        receiveShadow
      >
        {wireframe ? (
          <meshBasicMaterial color="#00ff00" wireframe />
        ) : (
          <meshStandardMaterial
            color="#888888"
            metalness={0.8}
            roughness={0.2}
          />
        )}
      </mesh>

      {/* Dimension labels */}
      {showDimensions && (
        <>
          <DimensionLine
            start={[bbox.min.x, bbox.min.y, bbox.min.z]}
            end={[bbox.max.x, bbox.min.y, bbox.min.z]}
            label={`${dimensions.x.toFixed(1)}mm`}
            color="#ff0000"
          />
          <DimensionLine
            start={[bbox.min.x, bbox.min.y, bbox.min.z]}
            end={[bbox.min.x, bbox.max.y, bbox.min.z]}
            label={`${dimensions.y.toFixed(1)}mm`}
            color="#00ff00"
          />
          <DimensionLine
            start={[bbox.min.x, bbox.min.y, bbox.min.z]}
            end={[bbox.min.x, bbox.min.y, bbox.max.z]}
            label={`${dimensions.z.toFixed(1)}mm`}
            color="#0000ff"
          />
        </>
      )}
    </group>
  )
}

/**
 * Dimension line component
 */
function DimensionLine({ start, end, label, color }: {
  start: [number, number, number]
  end: [number, number, number]
  label: string
  color: string
}) {
  const points = [new THREE.Vector3(...start), new THREE.Vector3(...end)]
  const geometry = new THREE.BufferGeometry().setFromPoints(points)

  return (
    <group>
      <line geometry={geometry}>
        <lineBasicMaterial color={color} linewidth={2} />
      </line>
      {/* TODO: Add text label using Text component from @react-three/drei */}
    </group>
  )
}

/**
 * Loading fallback
 */
function LoadingFallback() {
  return (
    <mesh>
      <boxGeometry args={[1, 1, 1]} />
      <meshStandardMaterial color="#666666" wireframe />
    </mesh>
  )
}
