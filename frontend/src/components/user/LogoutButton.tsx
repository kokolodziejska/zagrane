import { Button } from '../ui/button';
import { useAppDispatch } from '@/store/hooks';
import { logout } from '@/store/userState';

function LogoutButton() {
  const dispatch = useAppDispatch();

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
    <>
      <Button type="button" variant="secondary" onClick={() => handleLogout()}>wyloguj się</Button>
    </>
  );
}

export default LogoutButton;
