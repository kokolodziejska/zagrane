import DepartmentSetDate from "@/components/admin/menu pages/DepartmentSetDate";

function DepartmenSetDate() {
  return (
    <div className="w-full flex flex-col items-center py-10">
      <h1 className="text-3xl font-bold w-full text-center mb-8">
        Ustal terminy budżetowania
      </h1>

      <div className="w-[80vw]">
        <DepartmentSetDate />
      </div>
    </div>
  );
}

export default DepartmenSetDate;
