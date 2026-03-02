// 3D场景相关类型定义

export interface SceneConfig {
  backgroundColor?: string
  backgroundImage?: string
  backgroundIntensity?: number
  backgroundBlurriness?: number
  environmentMap?: string
}

export interface LightConfig {
  ambientLight: {
    enabled: boolean
    color: string
    intensity: number
  }
  directionalLight: {
    enabled: boolean
    color: string
    intensity: number
    position: { x: number; y: number; z: number }
    castShadow: boolean
  }
  pointLight: {
    enabled: boolean
    color: string
    intensity: number
    position: { x: number; y: number; z: number }
  }
}

export interface ModelConfig {
  id: string
  name: string
  filePath: string
  fileType: 'glb' | 'gltf' | 'obj' | 'fbx'
  position: { x: number; y: number; z: number }
  rotation: { x: number; y: number; z: number }
  scale: number
  visible: boolean
  userData?: Record<string, any>
}

export interface HelperConfig {
  gridHelper: {
    enabled: boolean
    size: number
    divisions: number
    color: string
  }
  axesHelper: {
    enabled: boolean
    size: number
  }
  transformControls: {
    enabled: boolean
    mode: 'translate' | 'rotate' | 'scale'
  }
}

export const PREDEFINE_COLORS = [
  "#ff4500",
  "#ff8c00", 
  "#ffd700",
  "#90ee90",
  "#00ced1",
  "#1e90ff",
  "#c71585",
  "rgba(255, 69, 0, 0.68)",
  "rgb(255, 120, 0)",
  "hsv(51, 100, 98)",
  "hsva(120, 40, 94, 0.5)",
  "hsl(181, 100%, 37%)",
  "hsla(209, 100%, 56%, 0.73)",
  "#c7158577"
]

export const MODEL_TYPE_ENUM = {
  OneModel: 'oneModel',
  ManyModel: 'manyModel', 
  Geometry: 'geometry',
  Tags: 'tags'
} as const
