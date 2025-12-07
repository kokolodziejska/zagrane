import DepartmentSetDate from "@/components/admin/menu pages/DepartmentSetDate";

function DepartmenSetDate() {
  return (
    <div className="overflow-hidden">
      <h1 className="text-3xl font-bold w-full text-center">Ustal terminy budżetowania</h1>
      <div className="container flex flex-col items-center justify-center w-[80vw] gap-[2vw] pb-[10vh] mt-[4vh]">
        <DepartmentSetDate />
      </div>
    </div>
  );
}

export default DepartmenSetDate;
