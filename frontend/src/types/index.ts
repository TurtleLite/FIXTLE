// Tipos de datos
export interface User {
  id: number
  username: string
  nombre_completo: string
  role: 'admin' | 'vendedor'
  activo: boolean
  created_at?: string
}

export interface LoginResponse {
  access_token: string
  token_type: string
  user: User
}

export interface Sale {
  id: number
  producto: string
  cantidad: number
  precio_unitario: number
  total: number
  fecha: string
  created_at?: string
  user_id: number
  vendedor?: string
}

export interface SaleList {
  items: Sale[]
  total: number
  count: number
}

export interface Expense {
  id: number
  descripcion: string
  monto: number
  categoria?: string
  fecha: string
  created_at?: string
  user_id: number
  usuario?: string
}

export interface ExpenseList {
  items: Expense[]
  total: number
  count: number
}

export interface Report {
  desde: string
  hasta: string
  total_ventas: number
  cantidad_ventas: number
  total_gastos: number
  cantidad_gastos: number
  ganancia_neta: number
}
