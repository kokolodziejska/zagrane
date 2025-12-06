import { BrowserRouter, Routes, Route } from 'react-router-dom';

import LoginPage from './pages/user/LoginPage';

import AdminLayout from './pages/admin/AdminLayout';
import DashBoard from './pages/admin/DashBoard';
import MangeUserPage from './pages/admin/dashboard/MangeUserPage';
import LimitBudgetPage from './pages/admin/dashboard/LimitBudgetPage';
import MangeBudgetPage from './pages/admin/dashboard/MangeBudgetPage';

function App() {
  return (
    <>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<LoginPage />} />

          <Route path="/admin" element={<AdminLayout />}>
            <Route index element={<DashBoard />} />
            <Route path="zarzadzaj-urzytkonikami" element={<MangeUserPage />} />
            <Route path="limity-budrzetu" element={<LimitBudgetPage />} />
            <Route path="limity-budrzetu" element={<MangeBudgetPage />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </>
  );
}

export default App;
