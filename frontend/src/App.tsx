import { BrowserRouter, Routes, Route } from 'react-router-dom';

import LoginPage from './pages/user/LoginPage';

import AdminLayout from './pages/admin/AdminLayout';
import DashBoard from './pages/admin/DashBoard';

function App() {
  return (
    <>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<LoginPage />} />

          <Route path="/admin" element={<AdminLayout />}>
            <Route index element={<DashBoard />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </>
  );
}

export default App;
