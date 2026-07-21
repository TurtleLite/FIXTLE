import { useState } from 'react'
import api from '../services/api'
import type { Report } from '../types'
import { Calendar, TrendingUp, DollarSign, FileText } from 'lucide-react'

export default function Reportes() {
  const [desde, setDesde] = useState('')
  const [hasta, setHasta] = useState('')
  const [report, setReport] = useState<Report | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!desde || !hasta) return
    setError('')
    setLoading(true)
    try {
      const desdeISO = new Date(desde + 'T00:00:00').toISOString()
      const hastaISO = new Date(hasta + 'T23:59:59').toISOString()
      const res = await api.get(`/reports?desde=${encodeURIComponent(desdeISO)}&hasta=${encodeURIComponent(hastaISO)}`)
      setReport(res.data)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Error al generar reporte')
    } finally {
      setLoading(false)
    }
  }

  const formatMoney = (n: number) => `$${n.toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ',')}`

  return (
    <div>
      <h2 className="text-lg font-semibold text-gray-800 mb-4">
        <FileText className="w-5 h-5 inline mr-2" />
        Reportes por Fecha
      </h2>

      <form onSubmit={handleSubmit} className="space-y-3 mb-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Fecha inicio
          </label>
          <input
            type="date"
            value={desde}
            onChange={(e) => setDesde(e.target.value)}
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none text-base"
            required
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Fecha fin
          </label>
          <input
            type="date"
            value={hasta}
            onChange={(e) => setHasta(e.target.value)}
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none text-base"
            required
          />
        </div>
        <button
          type="submit"
          disabled={loading}
          className="w-full bg-indigo-600 text-white py-3 rounded-lg font-medium hover:bg-indigo-700 disabled:opacity-50 transition-colors flex items-center justify-center gap-2"
        >
          <Calendar className="w-5 h-5" />
          {loading ? 'Generando...' : 'Generar Reporte'}
        </button>
      </form>

      {error && (
        <div className="bg-red-50 text-red-600 text-sm p-3 rounded-lg border border-red-200 mb-4">
          {error}
        </div>
      )}

      {report && (
        <div className="space-y-3">
          <div className="text-center text-sm text-gray-500 mb-2">
            Reporte del {new Date(report.desde).toLocaleDateString('es-MX')} al {new Date(report.hasta).toLocaleDateString('es-MX')}
          </div>

          <div className="bg-green-50 border border-green-200 rounded-xl p-4">
            <div className="flex items-center gap-2 text-green-700 mb-1">
              <TrendingUp className="w-5 h-5" />
              <p className="text-sm font-medium">Ventas</p>
            </div>
            <p className="text-2xl font-bold text-green-600">{formatMoney(report.total_ventas)}</p>
            <p className="text-xs text-green-500">{report.cantidad_ventas} ventas realizadas</p>
          </div>

          <div className="bg-red-50 border border-red-200 rounded-xl p-4">
            <div className="flex items-center gap-2 text-red-700 mb-1">
              <DollarSign className="w-5 h-5" />
              <p className="text-sm font-medium">Gastos</p>
            </div>
            <p className="text-2xl font-bold text-red-500">{formatMoney(report.total_gastos)}</p>
            <p className="text-xs text-red-500">{report.cantidad_gastos} gastos registrados</p>
          </div>

          <div className={`border-2 rounded-xl p-4 ${
            report.ganancia_neta >= 0
              ? 'bg-indigo-50 border-indigo-200'
              : 'bg-orange-50 border-orange-200'
          }`}>
            <p className="text-sm font-medium text-gray-700 mb-1">Ganancia Neta</p>
            <p className={`text-3xl font-bold ${
              report.ganancia_neta >= 0 ? 'text-indigo-600' : 'text-orange-600'
            }`}>
              {formatMoney(report.ganancia_neta)}
            </p>
          </div>
        </div>
      )}

      {!report && !loading && (
        <div className="text-center text-gray-400 py-8">
          <Calendar className="w-12 h-12 mx-auto mb-2 opacity-50" />
          <p>Selecciona un rango de fechas y genera tu reporte</p>
        </div>
      )}
    </div>
  )
}
