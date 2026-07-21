import { useState } from 'react'
import api from '../services/api'
import { Check, X } from 'lucide-react'

interface Props {
  onSuccess: () => void
}

export default function RegistrarGasto({ onSuccess }: Props) {
  const [descripcion, setDescripcion] = useState('')
  const [monto, setMonto] = useState('')
  const [categoria, setCategoria] = useState('')
  const [loading, setLoading] = useState(false)
  const [success, setSuccess] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      const fecha = new Date().toISOString()
      await api.post('/expenses', {
        descripcion,
        monto: parseFloat(monto),
        categoria: categoria || null,
        fecha,
      })
      setSuccess(true)
      setDescripcion('')
      setMonto('')
      setCategoria('')
      onSuccess()
      setTimeout(() => setSuccess(false), 2000)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Error al registrar gasto')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <h2 className="text-lg font-semibold text-gray-800 mb-4">Registrar Gasto</h2>

      {success && (
        <div className="bg-green-50 text-green-700 p-3 rounded-lg mb-4 flex items-center gap-2 border border-green-200">
          <Check className="w-5 h-5" />
          Gasto registrado correctamente
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Descripción
          </label>
          <input
            type="text"
            value={descripcion}
            onChange={(e) => setDescripcion(e.target.value)}
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none text-base"
            placeholder="Ej: Luz del local, Compra de inventario..."
            required
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Monto ($)
          </label>
          <input
            type="number"
            step="0.01"
            min="0.01"
            value={monto}
            onChange={(e) => setMonto(e.target.value)}
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none text-base"
            placeholder="0.00"
            required
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Categoría (opcional)
          </label>
          <select
            value={categoria}
            onChange={(e) => setCategoria(e.target.value)}
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none text-base bg-white"
          >
            <option value="">Sin categoría</option>
            <option value="Servicios">Servicios</option>
            <option value="Inventario">Inventario</option>
            <option value="Transporte">Transporte</option>
            <option value="Comida">Comida</option>
            <option value="Otros">Otros</option>
          </select>
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
          className="w-full bg-red-500 text-white py-3 rounded-lg font-medium hover:bg-red-600 disabled:opacity-50 transition-colors"
        >
          {loading ? 'Registrando...' : 'Registrar Gasto'}
        </button>
      </form>
    </div>
  )
}
