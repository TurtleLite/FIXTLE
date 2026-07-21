import { useState } from 'react'
import api from '../services/api'
import { Check, X } from 'lucide-react'

interface Props {
  onSuccess: () => void
}

export default function RegistrarVenta({ onSuccess }: Props) {
  const [producto, setProducto] = useState('')
  const [cantidad, setCantidad] = useState(1)
  const [precio, setPrecio] = useState('')
  const [loading, setLoading] = useState(false)
  const [success, setSuccess] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      const fecha = new Date().toISOString()
      await api.post('/sales', {
        producto,
        cantidad,
        precio_unitario: parseFloat(precio),
        fecha,
      })
      setSuccess(true)
      setProducto('')
      setCantidad(1)
      setPrecio('')
      onSuccess()
      setTimeout(() => setSuccess(false), 2000)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Error al registrar venta')
    } finally {
      setLoading(false)
    }
  }

  const total = cantidad * (parseFloat(precio) || 0)

  return (
    <div>
      <h2 className="text-lg font-semibold text-gray-800 mb-4">Registrar Venta</h2>

      {success && (
        <div className="bg-green-50 text-green-700 p-3 rounded-lg mb-4 flex items-center gap-2 border border-green-200">
          <Check className="w-5 h-5" />
          Venta registrada correctamente
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Producto
          </label>
          <input
            type="text"
            value={producto}
            onChange={(e) => setProducto(e.target.value)}
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none text-base"
            placeholder="Ej: Collar de plata"
            required
          />
        </div>

        <div className="grid grid-cols-2 gap-3">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Cantidad
            </label>
            <input
              type="number"
              min={1}
              value={cantidad}
              onChange={(e) => setCantidad(parseInt(e.target.value) || 1)}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none text-base"
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Precio unitario ($)
            </label>
            <input
              type="number"
              step="0.01"
              min="0.01"
              value={precio}
              onChange={(e) => setPrecio(e.target.value)}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none text-base"
              placeholder="0.00"
              required
            />
          </div>
        </div>

        {/* Total en vivo */}
        <div className="bg-indigo-50 rounded-lg p-3 text-center">
          <p className="text-xs text-gray-500">Total</p>
          <p className="text-2xl font-bold text-indigo-700">${total.toFixed(2)}</p>
        </div>

        {error && (
          <div className="bg-red-50 text-red-600 text-sm p-3 rounded-lg border border-red-200 flex items-center gap-2">
            <X className="w-4 h-4" />
            {error}
          </div>
        )}

        <button
          type="submit"
          disabled={loading}
          className="w-full bg-indigo-600 text-white py-3 rounded-lg font-medium hover:bg-indigo-700 disabled:opacity-50 transition-colors"
        >
          {loading ? 'Registrando...' : 'Registrar Venta'}
        </button>
      </form>
    </div>
  )
}
