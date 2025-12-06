import { BrowserRouter, Routes, Route } from 'react-router-dom';

import LoginPage from './pages/user/LoginPage';

import AdminLayout from './pages/admin/AdminLayout';
import DashBoard from './pages/admin/DashBoard';
import MangeUserPage from './pages/admin/AdminReservations';

function App() {
  return (
    <>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<LoginPage />} />

          <Route path="/admin" element={<AdminLayout />}>
            <Route index element={<DashBoard />} />
            <Route path="/zarzadzaj-urzytkonikami" element={<MangeUserPage />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </>
  );
}

export default App;
