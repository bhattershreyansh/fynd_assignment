import { useState } from 'react';
import { LayoutDashboard, FileText, AlertTriangle, LogOut } from 'lucide-react';
import DashboardTab from './admin/DashboardTab';
import AllReviewsTab from './admin/AllReviewsTab';
import PriorityReviewsTab from './admin/PriorityReviewsTab';

type TabType = 'dashboard' | 'all-reviews' | 'priority';

export default function AdminDashboard() {
  const [activeTab, setActiveTab] = useState<TabType>('dashboard');

  const handleSignOut = () => {
    window.location.href = '/';
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <header className="bg-gray-900 text-white shadow-lg">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center gap-3">
              <div className="bg-white text-gray-900 rounded-lg p-2">
                <FileText className="w-6 h-6" />
              </div>
              <div>
                <h1 className="text-2xl font-bold">Review Admin</h1>
                <p className="text-gray-400 text-sm">Management Dashboard</p>
              </div>
            </div>
          </div>

          <nav className="flex gap-2">
            <button
              onClick={() => setActiveTab('dashboard')}
              className={`flex items-center gap-2 px-4 py-2 rounded-lg font-medium transition-colors ${
                activeTab === 'dashboard'
                  ? 'bg-white text-gray-900'
                  : 'text-gray-300 hover:bg-gray-800'
              }`}
            >
              <LayoutDashboard className="w-4 h-4" />
              Dashboard
            </button>
            <button
              onClick={() => setActiveTab('all-reviews')}
              className={`flex items-center gap-2 px-4 py-2 rounded-lg font-medium transition-colors ${
                activeTab === 'all-reviews'
                  ? 'bg-white text-gray-900'
                  : 'text-gray-300 hover:bg-gray-800'
              }`}
            >
              <FileText className="w-4 h-4" />
              All Reviews
            </button>
            <button
              onClick={() => setActiveTab('priority')}
              className={`flex items-center gap-2 px-4 py-2 rounded-lg font-medium transition-colors ${
                activeTab === 'priority'
                  ? 'bg-white text-gray-900'
                  : 'text-gray-300 hover:bg-gray-800'
              }`}
            >
              <AlertTriangle className="w-4 h-4" />
              Priority Reviews
            </button>
            <button
              onClick={handleSignOut}
              className="flex items-center gap-2 px-4 py-2 rounded-lg font-medium text-red-400 hover:bg-gray-800 transition-colors ml-auto"
            >
              <LogOut className="w-4 h-4" />
              Sign Out
            </button>
          </nav>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-8">
        {activeTab === 'dashboard' && <DashboardTab />}
        {activeTab === 'all-reviews' && <AllReviewsTab />}
        {activeTab === 'priority' && <PriorityReviewsTab />}
      </main>
    </div>
  );
}
