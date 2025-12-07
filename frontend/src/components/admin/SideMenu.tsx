import {
  Sidebar,
  SidebarHeader,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarGroupContent,
  SidebarMenu,
  SidebarMenuItem,
  SidebarMenuButton,
} from '@/components/ui/sidebar';

import {
  DropdownMenu,
  DropdownMenuTrigger,
  DropdownMenuContent,
  DropdownMenuItem,
} from '@/components/ui/dropdown-menu';

import { User2, ChevronUp } from 'lucide-react';
import ContentSideBarMenu from './ContentSideBarMenu';
import { useAppDispatch } from '@/store/hooks';
import { logout } from '@/store/userState';
import { useNavigate } from 'react-router-dom';

export default function SideMenu() {
  const dispatch = useAppDispatch();
  const navigate = useNavigate();

  const handleLogout = async (): Promise<void> => {
    try {
      const res = await fetch(`/api/user/logout`, {
        method: 'POST',
        credentials: 'include',
      });
      dispatch(logout());
    } catch (err) {
      dispatch(logout());
      return;
    }
  };
  return (
    <div className="h-full min-h-0">
      <Sidebar
        side="left"
        variant="sidebar"
        collapsible="offcanvas"
        className="top-[10vh] h-[90vh]"
      >
        <SidebarHeader />
        <SidebarContent>
          <SidebarGroup>
            <SidebarGroupContent>
              <SidebarMenu>
                <ContentSideBarMenu />
              </SidebarMenu>
            </SidebarGroupContent>
          </SidebarGroup>
        </SidebarContent>

        <SidebarFooter>
          <SidebarMenu>
            <SidebarMenuItem>
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <SidebarMenuButton aria-label="User menu">
                    <User2 />
                    <span className="ml-2">Administrator</span>
                    <ChevronUp className="ml-auto" />
                  </SidebarMenuButton>
                </DropdownMenuTrigger>
                <DropdownMenuContent side="top" className="w-[--radix-popper-anchor-width]">
                  <DropdownMenuItem onClick={() => (handleLogout(), navigate('/'))}>
                    Wyloguj
                  </DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>
            </SidebarMenuItem>
          </SidebarMenu>
        </SidebarFooter>
      </Sidebar>
    </div>
  );
}
