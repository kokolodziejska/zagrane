import SideMenu from '@/components/admin/SideMenu';
import { Outlet } from 'react-router-dom';
import HeaderAdmin from '@/components/admin/HeaderAdmin';

import { SidebarProvider, SidebarTrigger } from '@/components/ui/sidebar';
import { Menu } from 'lucide-react';

function AdminLayout() {
  return (
    <div className="flex h-[100vh] flex-col overflow-hidden">
      <HeaderAdmin />
      <div
        className="flex flex-1 h-[80vh] overflow-hidden"
      >
        <SidebarProvider>
          <div className="flex flex-1 min-h-0 overflow-hidden">
            <SideMenu />
            <main className="flex-1 p-4 overflow-auto">
              <div className="flex flex-row">
                <SidebarTrigger aria-label="Open sidebar" className="mb-4">
                  <Menu className="w-5 h-5" />
                </SidebarTrigger>{' '}
                <div className="flex-1 w-full overflow-y-auto flex flex-col items-center gap-[1vh]">
                  <Outlet />
                </div>
              </div>
            </main>
          </div>
        </SidebarProvider>
      </div>
    </div>
  );
}

export default AdminLayout;
