import LimitBudget from '@/components/admin/menu pages/LimitBudget';

function LimitBudgetPage() {
  return (
    <div className="overflow-hidden">
      <h1 className="text-3xl font-bold w-full text-center">Ustal limity budżetu</h1>
      <div className="container flex flex-col items-center justify-center w-[80vw] gap-[2vw] pb-[10vh] mt-[4vh]">
        <LimitBudget />
      </div>
    </div>
  );
}

export default LimitBudgetPage;
