import MangeUser from '@/components/admin/menu pages/MangedUsers';

function MangeUserPage() {
  return (
    <div>
      <div className="container flex flex-col items-center justify-center w-[80vw] margin-[5vh] gap-[2vw] pb-[10vh]">
        <MangeUser />
      </div>
    </div>
  );
}

export default MangeUserPage;
