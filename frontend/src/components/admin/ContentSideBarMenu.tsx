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
            to="/admin/zarzadzajRezerwacjami"
            className={({ isActive }) => (isActive ? 'bg-muted font-medium' : undefined)}
          >
            Zarządzaj rezerwacjami
          </NavLink>
        </SidebarMenuButton>
      </SidebarMenuItem>

      <SidebarMenuItem>
        <SidebarMenuButton asChild>
          <NavLink
            to="/admin/statystyki"
            className={({ isActive }) => (isActive ? 'bg-muted font-medium' : undefined)}
          >
            Statystyki
          </NavLink>
        </SidebarMenuButton>
      </SidebarMenuItem>

      {/* Sekcje wysuwane */}
      <Collapsible defaultOpen className="group/collapsible">
        <SidebarMenuItem>
          <CollapsibleTrigger asChild>
            <SidebarMenuButton>
              <span>Dane firmy</span>
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
                    Globalne
                  </NavLink>
                </SidebarMenuSubButton>
              </SidebarMenuSubItem>

              <SidebarMenuSubItem>
                <SidebarMenuSubButton asChild>
                  <NavLink
                    to="/admin/UstawieniaObiektow"
                    className={({ isActive }) => (isActive ? 'bg-muted font-medium' : undefined)}
                  >
                    Obiekty
                  </NavLink>
                </SidebarMenuSubButton>
              </SidebarMenuSubItem>

              <SidebarMenuSubItem>
                <SidebarMenuSubButton asChild>
                  <NavLink
                    to="/admin/UstawieniaCennika"
                    className={({ isActive }) => (isActive ? 'bg-muted font-medium' : undefined)}
                  >
                    Cennik
                  </NavLink>
                </SidebarMenuSubButton>
              </SidebarMenuSubItem>
            </SidebarMenuSub>
          </CollapsibleContent>
        </SidebarMenuItem>
      </Collapsible>

      <Collapsible defaultOpen className="group/collapsible">
        <SidebarMenuItem>
          <CollapsibleTrigger asChild>
            <SidebarMenuButton>
              <span>Strona</span>
              <ChevronDown className="ml-auto" />
            </SidebarMenuButton>
          </CollapsibleTrigger>

          <CollapsibleContent>
            <SidebarMenuSub>
              <SidebarMenuSubItem>
                <SidebarMenuSubButton asChild>
                  <NavLink to="/projekty/1">Strona główna</NavLink>
                </SidebarMenuSubButton>
              </SidebarMenuSubItem>
              <SidebarMenuSubItem>
                <SidebarMenuSubButton asChild>
                  <NavLink to="/projekty/2">O nas</NavLink>
                </SidebarMenuSubButton>
              </SidebarMenuSubItem>
              <SidebarMenuSubItem>
                <SidebarMenuSubButton asChild>
                  <NavLink to="/projekty/3">Kontakt</NavLink>
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
