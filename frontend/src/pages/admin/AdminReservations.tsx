import ManageReservations from '@/components/admin/reservations/ManageReservations';

function AdminReservations() {
  return (
    <div>
      <div className="container flex flex-col items-center justify-center w-[80vw] margin-[5vh] gap-[2vw] pb-[10vh]">
        <ManageReservations />
      </div>
    </div>
  );
}

export default AdminReservations;
