import { useState, useEffect } from 'react'
import { useAuth } from '../contexts/AuthContext'
import api from '../services/api'
import { ShoppingBag, DollarSign, TrendingUp, Plus, LogOut } from 'lucide-react'
import type { SaleList, ExpenseList, Report } from '../types'
import RegistrarVenta from './RegistrarVenta'
import RegistrarGasto from './RegistrarGasto'
import Reportes from './Reportes'

type Tab = 'resumen' | 'venta' | 'gasto' | 'reportes'

export default function Dashboard() {
  const { user, logout } = useAuth()
  const [activeTab, setActiveTab] = useState<Tab>('resumen')
  const [sales, setSales] = useState<SaleList | null>(null)
  const [expenses, setExpenses] = useState<ExpenseList | null>(null)
  const [report, setReport] = useState<Report | null>(null)
  const loadData = async () => {
    try {
      const hoy = new Date()
      hoy.setHours(0, 0, 0, 0)
      const manana = new Date(hoy)
      manana.setDate(manana.getDate() + 1)

      const [salesRes, expensesRes, reportRes] = await Promise.all([
        api.get(`/sales?desde=${hoy.toISOString()}&hasta=${manana.toISOString()}`),
        api.get(`/expenses?desde=${hoy.toISOString()}&hasta=${manana.toISOString()}`),
        api.get(`/reports?desde=${hoy.toISOString()}&hasta=${manana.toISOString()}`),
      ])
      setSales(salesRes.data)
      setExpenses(expensesRes.data)
      setReport(reportRes.data)
    } catch (err) {
      console.error('Error cargando datos:', err)
    }
  }

  useEffect(() => {
    loadData()
  }, [])

  const tabs = [
    { id: 'resumen' as Tab, label: 'Resumen', icon: TrendingUp },
    { id: 'venta' as Tab, label: 'Venta', icon: Plus },
    { id: 'gasto' as Tab, label: 'Gasto', icon: DollarSign },
    { id: 'reportes' as Tab, label: 'Reportes', icon: ShoppingBag },
  ]

  const formatMoney = (n: number) => `$${n.toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ',')}`
  const userInfo = user ? `${user.nombre_completo} (${user.role === 'admin' ? 'Admin' : 'Vendedor'})` : ''


  return (
    <div className="min-h-screen bg-gray-50 max-w-2xl mx-auto">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 px-4 py-3 sticky top-0 z-10">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-lg font-bold text-gray-900">Inversiones Espinoza</h1>
            <p className="text-xs text-gray-500">{userInfo}</p>
          </div>
          <button
            onClick={logout}
            className="p-2 text-gray-400 hover:text-red-500 transition-colors rounded-lg hover:bg-red-50"
            title="Cerrar sesión"
          >
            <LogOut className="w-5 h-5" />
          </button>
        </div>
        <div className="mt-1 text-xs text-gray-400">
          🕐 Horario: 8:00 AM - 6:00 PM
        </div>
      </header>

      {/* Navegación inferior */}
      <nav className="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 z-10 max-w-2xl mx-auto">
        <div className="flex justify-around py-2">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex flex-col items-center px-3 py-1 text-xs transition-colors ${
                activeTab === tab.id
                  ? 'text-indigo-600'
                  : 'text-gray-400 hover:text-gray-600'
              }`}
            >
              <tab.icon className="w-5 h-5 mb-1" />
              <span>{tab.label}</span>
            </button>
          ))}
        </div>
      </nav>

      {/* Contenido */}
      <main className="pb-20 px-4 pt-4">
        {activeTab === 'resumen' && (
          <div className="space-y-4">
            {/* Cards */}
            <div className="grid grid-cols-2 gap-3">
              <div className="bg-white p-4 rounded-xl shadow-sm border border-gray-100">
                <p className="text-xs text-gray-500 mb-1">Ventas hoy</p>
                <p className="text-xl font-bold text-green-600">
                  {report ? formatMoney(report.total_ventas) : '$0.00'}
                </p>
                <p className="text-xs text-gray-400">{report?.cantidad_ventas || 0} ventas</p>
              </div>
              <div className="bg-white p-4 rounded-xl shadow-sm border border-gray-100">
                <p className="text-xs text-gray-500 mb-1">Gastos hoy</p>
                <p className="text-xl font-bold text-red-500">
                  {report ? formatMoney(report.total_gastos) : '$0.00'}
                </p>
                <p className="text-xs text-gray-400">{report?.cantidad_gastos || 0} gastos</p>
              </div>
            </div>

            {/* Ganancia */}
            <div className="bg-white p-4 rounded-xl shadow-sm border border-gray-100">
              <p className="text-xs text-gray-500 mb-1">Ganancia del día</p>
              <p className={`text-2xl font-bold ${
                report && report.ganancia_neta >= 0 ? 'text-green-600' : 'text-red-500'
              }`}>
                {report ? formatMoney(report.ganancia_neta) : '$0.00'}
              </p>
            </div>

            {/* Últimas ventas */}
            <div>
              <h2 className="text-sm font-semibold text-gray-700 mb-2">Últimas ventas</h2>
              {sales && sales.items.length > 0 ? (
                <div className="space-y-2">
                  {sales.items.slice(0, 5).map((sale) => (
                    <div key={sale.id} className="bg-white p-3 rounded-lg shadow-sm border border-gray-100 flex justify-between items-center">
                      <div>
                        <p className="font-medium text-sm">{sale.producto}</p>
                        <p className="text-xs text-gray-500">
                          {new Date(sale.fecha).toLocaleTimeString('es-MX', { hour: '2-digit', minute: '2-digit' })} · {sale.cantidad} x ${sale.precio_unitario.toFixed(2)}
                        </p>
                      </div>
                      <p className="font-semibold text-green-600">${sale.total.toFixed(2)}</p>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="bg-white p-4 rounded-lg text-center text-gray-400 text-sm">
                  No hay ventas registradas hoy
                </div>
              )}
            </div>
          </div>
        )}

        {activeTab === 'venta' && <RegistrarVenta onSuccess={loadData} />}
        {activeTab === 'gasto' && <RegistrarGasto onSuccess={loadData} />}
        {activeTab === 'reportes' && <Reportes />}
      </main>
    </div>
  )
}

