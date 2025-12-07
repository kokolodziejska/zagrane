import { NavLink } from 'react-router-dom';

import {
  SidebarMenuItem,
  SidebarMenuButton,
  SidebarMenuSub,
  SidebarMenuSubItem,
  SidebarMenuSubButton,
} from '@/components/ui/sidebar';

import { Collapsible, CollapsibleTrigger, CollapsibleContent } from '@/components/ui/collapsible';
import { ChevronDown } from 'lucide-react';

function ContentSideBarMenu() {
  return (
    <>
      {/* Zwykłe elementy bez sekcji */}
      <SidebarMenuItem>
        <SidebarMenuButton asChild>
          <NavLink
            to="/admin"
            className={({ isActive }) => (isActive ? 'bg-muted font-medium' : undefined)}
          >
            Panel główny
          </NavLink>
        </SidebarMenuButton>
      </SidebarMenuItem>

      <SidebarMenuItem>
        <SidebarMenuButton asChild>
          <NavLink
            to="/admin/zarzadzaj-budzetem"
            className={({ isActive }) => (isActive ? 'bg-muted font-medium' : undefined)}
          >
            Zarządzaj budżetem
          </NavLink>
        </SidebarMenuButton>
      </SidebarMenuItem>

      <SidebarMenuItem>
        <SidebarMenuButton asChild>
          <NavLink
            to="/admin/uwagi-do-budżetu"
            className={({ isActive }) => (isActive ? 'bg-muted font-medium' : undefined)}
          >
            Uwagi do budżetu
          </NavLink>
        </SidebarMenuButton>
      </SidebarMenuItem>

      <SidebarMenuItem>
        <SidebarMenuButton asChild>
          <NavLink
            to="/admin/limity-budzetu"
            className={({ isActive }) => (isActive ? 'bg-muted font-medium' : undefined)}
          >
            Limity budżetu
          </NavLink>
        </SidebarMenuButton>
      </SidebarMenuItem>

      <SidebarMenuItem>
        <SidebarMenuButton asChild>
          <NavLink
            to="/admin/terminy-budzetowania"
            className={({ isActive }) => (isActive ? 'bg-muted font-medium' : undefined)}
          >
            Terminy budżetowania
          </NavLink>
        </SidebarMenuButton>
      </SidebarMenuItem>

      <SidebarMenuItem>
        <SidebarMenuButton asChild>
          <NavLink
            to="/admin/zarzadzaj-urzytkonikami"
            className={({ isActive }) => (isActive ? 'bg-muted font-medium' : undefined)}
          >
            Zarządzaj użytkonikami
          </NavLink>
        </SidebarMenuButton>
      </SidebarMenuItem>

      {/* Sekcje wysuwane */}
      <Collapsible defaultOpen className="group/collapsible">
        <SidebarMenuItem>
          <CollapsibleTrigger asChild>
            <SidebarMenuButton>
              <span>Zobacz budżet</span>
              <ChevronDown className="ml-auto" />
            </SidebarMenuButton>
          </CollapsibleTrigger>

          <CollapsibleContent>
            <SidebarMenuSub>
              <SidebarMenuSubItem>
                <SidebarMenuSubButton asChild>
                  <NavLink
                    to="/admin/UstawieniaGlobalne"
                    className={({ isActive }) => (isActive ? 'bg-muted font-medium' : undefined)}
                  >
                    2025
                  </NavLink>
                </SidebarMenuSubButton>
              </SidebarMenuSubItem>

              <SidebarMenuSubItem>
                <SidebarMenuSubButton asChild>
                  <NavLink
                    to="/admin/UstawieniaGlobalne"
                    className={({ isActive }) => (isActive ? 'bg-muted font-medium' : undefined)}
                  >
                    2026
                  </NavLink>
                </SidebarMenuSubButton>
              </SidebarMenuSubItem>

              <SidebarMenuSubItem>
                <SidebarMenuSubButton asChild>
                  <NavLink
                    to="/admin/UstawieniaGlobalne"
                    className={({ isActive }) => (isActive ? 'bg-muted font-medium' : undefined)}
                  >
                    2027
                  </NavLink>
                </SidebarMenuSubButton>
              </SidebarMenuSubItem>

              <SidebarMenuSubItem>
                <SidebarMenuSubButton asChild>
                  <NavLink
                    to="/admin/UstawieniaGlobalne"
                    className={({ isActive }) => (isActive ? 'bg-muted font-medium' : undefined)}
                  >
                    2028
                  </NavLink>
                </SidebarMenuSubButton>
              </SidebarMenuSubItem>
            </SidebarMenuSub>
          </CollapsibleContent>
        </SidebarMenuItem>
      </Collapsible>
    </>
  );
}

export default ContentSideBarMenu;
