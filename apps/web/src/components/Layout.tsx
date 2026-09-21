import React, { useState } from 'react';
import { NavLink, Outlet } from 'react-router-dom';
import { LayoutDashboard, FileSearch, ArrowRightLeft, Activity, FileText, Menu, X } from 'lucide-react';
import { SyntheticBadge } from './SyntheticBadge';
import { Footer } from './Footer';
import clsx from 'clsx';

const navItems = [
  { name: 'Overview', path: '/demo/overview', icon: LayoutDashboard },
  { name: 'Findings', path: '/demo/findings', icon: FileSearch },
  { name: 'Reconciliation', path: '/demo/reconciliation', icon: ArrowRightLeft },
  { name: 'Tracking Health', path: '/demo/tracking-health', icon: Activity },
  { name: 'Reports', path: '/demo/reports', icon: FileText },
];

export const Layout: React.FC = () => {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      {/* Mobile sidebar backdrop */}
      {sidebarOpen && (
        <div 
          className="fixed inset-0 z-20 bg-gray-900/50 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Top Header */}
      <header className="bg-white border-b border-gray-200 flex items-center justify-between px-4 sm:px-6 lg:px-8 h-16 shrink-0 z-10 sticky top-0">
        <div className="flex items-center">
          <button 
            className="lg:hidden p-2 -ml-2 mr-2 text-gray-500 hover:text-gray-700"
            onClick={() => setSidebarOpen(true)}
          >
            <Menu className="w-6 h-6" />
          </button>
          <h1 className="text-xl font-bold text-gray-900 tracking-tight">Commerce Truth Lab</h1>
        </div>
        <div className="hidden sm:block">
          <SyntheticBadge compact />
        </div>
      </header>

      <div className="flex flex-1 overflow-hidden">
        {/* Sidebar */}
        <aside className={clsx(
          "fixed inset-y-0 left-0 z-30 w-64 bg-white border-r border-gray-200 transform transition-transform duration-200 ease-in-out lg:translate-x-0 lg:static lg:inset-auto",
          sidebarOpen ? "translate-x-0" : "-translate-x-full"
        )}>
          <div className="h-full flex flex-col">
            <div className="flex items-center justify-between h-16 px-4 lg:hidden border-b border-gray-200">
              <span className="font-bold text-lg">Menu</span>
              <button onClick={() => setSidebarOpen(false)} className="text-gray-500 hover:text-gray-700">
                <X className="w-6 h-6" />
              </button>
            </div>
            <nav className="flex-1 px-4 py-6 space-y-1 overflow-y-auto">
              {navItems.map((item) => {
                const Icon = item.icon;
                return (
                  <NavLink
                    key={item.name}
                    to={item.path}
                    onClick={() => setSidebarOpen(false)}
                    className={({ isActive }) => clsx(
                      "flex items-center px-3 py-2.5 text-sm font-medium rounded-md group transition-colors",
                      isActive 
                        ? "bg-brand-50 text-brand-700" 
                        : "text-gray-700 hover:bg-gray-100 hover:text-gray-900"
                    )}
                  >
                    <Icon className={clsx(
                      "flex-shrink-0 w-5 h-5 mr-3",
                      "text-gray-400 group-hover:text-gray-500"
                    )} />
                    {item.name}
                  </NavLink>
                );
              })}
            </nav>
          </div>
        </aside>

        {/* Main content */}
        <main className="flex-1 flex flex-col min-w-0 overflow-y-auto overflow-x-hidden focus:outline-none">
          <div className="sm:hidden w-full">
            <SyntheticBadge />
          </div>
          <div className="flex-1 py-8 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto w-full">
            <Outlet />
          </div>
          <Footer />
        </main>
      </div>
    </div>
  );
};
