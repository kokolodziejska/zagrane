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

const tab = {
  headers: ['Dział', 'Potrzebny Budżet (zł)', 'Przydziel Budżet (zł)', 'Różnica'],
  rows: [
    ['Dział A', '50000', '48000', ''],
    ['Dział B', '70000', '68000', ''],
    ['Dział C', '30000', '32000', ''],
    ['Dział D', '30000', '32000', ''],
    ['Dział E', '30000', '32000', ''],
    ['Dział F', '30000', '32000', ''],
    ['Dział G', '30000', '32000', ''],
    ['Dział G', '30000', '32000', ''],
    ['Dział G', '30000', '32000', ''],
    ['Dział G', '30000', '32000', ''],
    ['Dział G', '30000', '32000', ''],
    ['Dział G', '30000', '32000', ''],
    ['Dział G', '30000', '32000', ''],
    ['Dział G', '30000', '32000', ''],
    ['Dział G', '30000', '32000', ''],
  ],
};

function LimitBudget() {
  const [budgetLimit, setBudgetLimit] = useState('');
  const [assignedBudget, setAssignedBudget] = useState('');
  const [editedBudgets, setEditedBudgets] = useState(tab.rows.map((row) => row[2]));

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

  const handleEditedBudgetChange = (e: React.ChangeEvent<HTMLInputElement>, index: number) => {
    const newBudgets = [...editedBudgets];
    newBudgets[index] = e.target.value;
    setEditedBudgets(newBudgets);
  };

  const totalAssignedBudget = editedBudgets.reduce((total, value) => {
    return total + parseFloat(value || '0');
  }, 0);

  const remainingBudget = parseFloat(budgetLimit || '0') - totalAssignedBudget;

  const calculateColumnSum = (columnIndex: number) => {
    return tab.rows.reduce((sum, row, index) => {
      const value =
        columnIndex === 1
          ? parseFloat(row[1])
          : columnIndex === 2
            ? parseFloat(editedBudgets[index] || '0')
            : calculateDifference(parseFloat(row[1]), parseFloat(editedBudgets[index] || '0'));
      return sum + (isNaN(value) ? 0 : value);
    }, 0);
  };

  const totalNeededBudget = calculateColumnSum(1);
  const totalAssigned = calculateColumnSum(2);
  const totalDifference = calculateColumnSum(3);

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
            value={totalAssigned}
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
                    width: j === 0 ? '5vw' : '15vw',
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
              {tab.rows.map((row, r) => (
                <TableRow key={r} className="hover:bg-gray-50">
                  {row.map((ele, e) => (
                    <TableCell
                      key={e}
                      className={`px-4 py-2 text-left border-x border-y ${
                        e === 0 ? 'pl-4 font-medium' : 'text-center'
                      }`}
                      style={{
                        width: e === 0 ? '5vw' : '15vw',
                      }}
                    >
                      {e === 2 ? (
                        <Input
                          type="text"
                          value={editedBudgets[r]}
                          onChange={(event) => handleEditedBudgetChange(event, r)}
                          className="w-[11vw] text-center"
                        />
                      ) : e === 3 ? (
                        <Input
                          type="text"
                          value={calculateDifference(
                            parseFloat(row[1]),
                            parseFloat(editedBudgets[r] || '0')
                          )}
                          readOnly
                          className="w-full bg-gray-100 text-gray-700 cursor-default text-center"
                        />
                      ) : (
                        ele
                      )}
                    </TableCell>
                  ))}
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
