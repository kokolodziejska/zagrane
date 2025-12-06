import AddComents from '@/components/admin/menu pages/AddComents';

function AddComentsPage() {
  return (
    <div>
      <h1 className="text-3xl font-bold w-full text-center">Dodaj uwagi do budrzetu</h1>
      <div className="container flex flex-col items-start justify-center w-[80vw] margin-[5vh] gap-[2vw] pb-[10vh]">
        <AddComents />
      </div>
    </div>
  );
}

export default AddComentsPage;
