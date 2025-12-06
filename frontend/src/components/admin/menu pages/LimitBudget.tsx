import { useState } from 'react';
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

// Definicja danych tabeli
const tab = {
  headers: ['Dział', 'Potrzebny Budżet', 'Przypisany Budżet'],
  rows: [
    ['Dział A', '50000 zł', '48000 zł'],
    ['Dział B', '70000 zł', '68000 zł'],
    ['Dział C', '30000 zł', '32000 zł'],
  ],
};

// Zmiana nazwy funkcji na LimitBudget
function LimitBudget() {
  const [budgetLimit, setBudgetLimit] = useState('');
  const [assignedBudget, setAssignedBudget] = useState('');

  // Jawne typowanie dla HTMLInputElement, aby usunąć błąd TS (e ma typ 'any')
  const handleBudgetLimitChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setBudgetLimit(e.target.value);
  };

  // Jawne typowanie dla HTMLInputElement
  const handleAssignedBudgetChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setAssignedBudget(e.target.value);
  };

  return (
    <div className="space-y-6">
      {/* Sekcja z polami dla zarządzania limitem */}
      <div className="flex space-x-4 items-end">
        <div className="flex-1">
          <Label htmlFor="budgetLimit">Nowy Limit Budżetu</Label>
          <Input
            id="budgetLimit"
            type="text"
            placeholder="Wpisz nowy limit"
            value={budgetLimit}
            onChange={handleBudgetLimitChange}
          />
        </div>
        <div className="flex-1">
          <Label htmlFor="assignedBudget">Przypisany Budżet</Label>
          <Input
            id="assignedBudget"
            type="text"
            placeholder="Wpisz przypisany budżet"
            value={assignedBudget}
            onChange={handleAssignedBudgetChange}
          />
        </div>
        <div className="flex-shrink-0">
          <Button
            onClick={() =>
              alert(`Zaktualizowano limit: ${budgetLimit}, przypisany budżet: ${assignedBudget}`)
            }
          >
            Zaktualizuj
          </Button>
        </div>
      </div>

      <hr className="my-6" />

      {/* Tabela budżetu działów */}
      <div className="overflow-x-auto max-h-[60vh] w-full">
        <Table className="min-w-max w-full">
          <TableCaption>Budżet Działów</TableCaption>
          <TableHeader className="bg-gray-100 sticky top-0 z-10">
            <TableRow>
              {tab.headers.map((header, j) => (
                <TableHead
                  key={j}
                  className="px-4 py-3 text-left font-bold text-gray-800 border-x border-y"
                >
                  {header}
                </TableHead>
              ))}
            </TableRow>
          </TableHeader>
          <TableBody>
            {tab.rows.map((row, r) => (
              <TableRow key={r} className="hover:bg-gray-50">
                {row.map((ele, e) => (
                  <TableCell
                    key={e}
                    className={`px-4 py-2 text-left border-x border-y ${e === 0 ? 'pl-4 font-medium' : ''}`}
                  >
                    {ele}
                  </TableCell>
                ))}
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
    </div>
  );
}

// Zmiana eksportowanej nazwy
export default LimitBudget;
