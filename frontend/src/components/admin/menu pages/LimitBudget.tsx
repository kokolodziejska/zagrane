import { useEffect, useState } from 'react';
import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';
import { Label } from '@/components/ui/label';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';

const tab = {
  headers: ['Dział', 'Potrzebny Budżet (zł)', 'Przydziel Budżet (zł)', 'Różnica'],
};


async function getNeedsPerDepartment() {
  try {
    const res = await fetch('/api/tables/1/get_needs_per_department');
    if (!res.ok) {
      throw new Error(`HTTP error! status: ${res.status}`);
    }
    return await res.json();
  } catch (err) {
    console.error('Error fetching needs per department:', err);
    return null;
  }
}

async function getLimitsPerDepartment() {
  try {
    const res = await fetch('/api/tables/1/get_limits_per_department');
    if (!res.ok) {
      throw new Error(`HTTP error! status: ${res.status}`);
    }
    return await res.json();
  } catch (err) {
    console.error('Error fetching limits per department:', err);
    return null;
  }
}

async function getTotalBudget() {
  try {
    const res = await fetch('/api/tables/1/get_total_budget');
    if (!res.ok) {
      throw new Error(`HTTP error! status: ${res.status}`);
    }
    // np. 1000000
    return await res.json(); // liczba
  } catch (err) {
    console.error('Error fetching total budget:', err);
    return null;
  }
}

type DepartmentRow = {
  name: string;   // nazwa działu (klucz z JSON)
  needed: number; // potrzebny budżet (wartość z JSON)
};

function LimitBudget() {
  const [budgetLimit, setBudgetLimit] = useState('');
  const [assignedBudget, setAssignedBudget] = useState(''); // zostawiam, może użyjesz później

  const [departments, setDepartments] = useState<DepartmentRow[]>([]);
  const [editedBudgets, setEditedBudgets] = useState<string[]>([]);

  useEffect(() => {
  (async () => {
    // 1) Pobranie potrzeb działów
    const needsData = await getNeedsPerDepartment();
    if (!needsData) return;

    const mapped: DepartmentRow[] = Object.entries(needsData).map(
      ([name, needed]) => ({
        name,
        needed: Number(needed),
      })
    );

    setDepartments(mapped);

    // 2) Pobranie globalnego limitu budżetu i ustawienie pola
    const totalBudget = await getTotalBudget();
    if (totalBudget !== null && totalBudget !== undefined) {
      setBudgetLimit(String(totalBudget));
    }

    // 3) Pobranie limitów per dział (3 kolumna tabeli)
    const limitsData = await getLimitsPerDepartment();

    if (limitsData) {
      setEditedBudgets(
        mapped.map((dep) =>
          limitsData[dep.name] !== undefined
            ? String(limitsData[dep.name])
            : ''
        )
      );
    } else {
      setEditedBudgets(mapped.map(() => ''));
    }
  })();
}, []);


  // Funkcja do obliczania różnicy
  const calculateDifference = (needed: number, assigned: number) => {
    return needed - assigned;
  };

  const handleBudgetLimitChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setBudgetLimit(e.target.value);
  };

  const handleAssignedBudgetChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setAssignedBudget(e.target.value);
  };

  const handleEditedBudgetChange = (
    e: React.ChangeEvent<HTMLInputElement>,
    index: number
  ) => {
    const newBudgets = [...editedBudgets];
    newBudgets[index] = e.target.value;
    setEditedBudgets(newBudgets);
  };

  const getAssigned = (index: number) =>
    parseFloat(editedBudgets[index] || '0');

  const totalNeededBudget = departments.reduce(
    (sum, dep) => sum + dep.needed,
    0
  );

  const totalAssignedBudget = departments.reduce(
    (sum, _dep, index) => sum + getAssigned(index),
    0
  );

  const remainingBudget = parseFloat(budgetLimit || '0') - totalAssignedBudget;

  const totalDifference = departments.reduce(
    (sum, dep, index) => sum + calculateDifference(dep.needed, getAssigned(index)),
    0
  );

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-3 grid-rows-1 gap-[1vw] h-[5vh]">
        <div className="flex flex-col justify-start">
          <Label htmlFor="budgetLimit" className="mb-2">
            Limit budżetu
          </Label>
          <Input
            id="budgetLimit"
            type="text"
            placeholder="Wpisz nowy limit"
            value={budgetLimit}
            onChange={handleBudgetLimitChange}
            className="flex-grow text-center"
          />
        </div>

        <div className="flex flex-col justify-start">
          <Label htmlFor="remainingBudget" className="mb-2">
            Pozostało
          </Label>
          <Input
            id="remainingBudget"
            type="text"
            value={remainingBudget}
            readOnly
            className="bg-gray-100 text-gray-700 cursor-default flex-grow text-center"
          />
        </div>
        <div className="flex flex-col justify-end items-end w-[15vw]">
          <Label htmlFor="remainingBudget" className="mb-2"></Label>
          <Button variant="default" className="h-[3.5vh] w-[7vw]">
            Zatwierdź
          </Button>
        </div>
      </div>

      <hr className="my-6" />

      <div className="flex flex-row justify-end gap-[2vw] h-[5vh] mb-[4vh] pr-[1vw]">
        <div className="flex flex-col justify-center items-center w-[13vw]">
          <Label htmlFor="sumaNeeded" className="mb-2">
            Suma Potrzebnego Budżetu
          </Label>
          <Input
            id="sumaNeeded"
            type="text"
            value={totalNeededBudget}
            readOnly
            className="bg-gray-100 text-gray-700 cursor-default flex-grow text-center"
          />
        </div>
        <div className="flex flex-col justify-center items-center w-[13vw]">
          <Label htmlFor="sumaAssigned" className="mb-2">
            Suma Przydzielonych Budżetów
          </Label>
          <Input
            id="sumaAssigned"
            type="text"
            value={totalAssignedBudget}
            readOnly
            className="bg-gray-100 text-gray-700 cursor-default flex-grow text-center"
          />
        </div>

        <div className="flex flex-col justify-center items-center w-[13vw]">
          <Label htmlFor="sumaDiff" className="mb-2">
            Suma Różnic
          </Label>
          <Input
            id="sumaDiff"
            type="text"
            value={totalDifference}
            readOnly
            className="bg-gray-100 text-gray-700 cursor-default flex-grow text-center"
          />
        </div>
      </div>

      <div>
        <Table className="min-w-max w-full">
          <TableHeader className="bg-gray-100 sticky top-0 z-10">
            <TableRow>
              {tab.headers.map((header, j) => (
                <TableHead
                  key={j}
                  className="px-4 py-3 text-left font-bold text-gray-800 border-x border-y text-center"
                  style={{
                    width: j === 0 ? '7vw' : '15vw',
                  }}
                >
                  {header}
                </TableHead>
              ))}
            </TableRow>
          </TableHeader>
        </Table>

        <div className="overflow-x-auto max-h-[55vh] scrollbar-hide">
          <Table className="min-w-max w-full">
            <TableBody>
              {departments.map((dep, r) => (
                <TableRow key={r} className="hover:bg-gray-50">
                  {/* kolumna 1 – nazwa działu */}
                  <TableCell
                    className="px-4 py-2 text-left border-x border-y pl-4 font-medium"
                    style={{ width: '7vw' }}
                  >
                    {dep.name}
                  </TableCell>

                  {/* kolumna 2 – potrzebny budżet */}
                  <TableCell
                    className="px-4 py-2 text-center border-x border-y"
                    style={{ width: '15vw' }}
                  >
                    {dep.needed}
                  </TableCell>

                  {/* kolumna 3 – przydziel budżet (wartości z endpointu + edycja) */}
                  <TableCell
                    className="px-4 py-2 text-center border-x border-y"
                    style={{ width: '15vw' }}
                  >
                    <Input
                      type="text"
                      value={editedBudgets[r] ?? ''}
                      onChange={(event) => handleEditedBudgetChange(event, r)}
                      className="w-[11vw] text-center"
                    />
                  </TableCell>

                  {/* kolumna 4 – różnica */}
                  <TableCell
                    className="px-4 py-2 text-center border-x border-y"
                    style={{ width: '15vw' }}
                  >
                    <Input
                      type="text"
                      value={calculateDifference(
                        dep.needed,
                        getAssigned(r)
                      )}
                      readOnly
                      className="w-full bg-gray-100 text-gray-700 cursor-default text-center"
                    />
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
      </div>
    </div>
  );
}

export default LimitBudget;
