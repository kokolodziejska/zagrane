import { useEffect, useState } from 'react';

import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';

import { Checkbox } from '@/components/ui/checkbox';
import { Button } from '@/components/ui/button';



const rows = [
  [
    'Funkcja Zadania 1',
    'Projekt A',
    'Jednostka A',
    'Plan 1',
    'Dystrybutor 1',
    50000,
    'Zadanie 1',
    'Uzasadnienie 1',
    'Cel 1',
    1000,
    1500,
    2000,
    500,
    1200,
    1000,
    600,
    1500,
    1300,
    1800,
    2500,
    1800,
    2200,
    2500,
    'UM001',
    'Strona A',
    'Podstawa A',
    'Uwagi A',
    'Dodatkowe A',
  ],
  [
    'Funkcja Zadania 2',
    'Projekt B',
    'Jednostka B',
    'Plan 2',
    'Dystrybutor 2',
    70000,
    'Zadanie 2',
    'Uzasadnienie 2',
    'Cel 2',
    1200,
    1600,
    1800,
    700,
    1300,
    1100,
    800,
    1600,
    1400,
    1900,
    2600,
    1900,
    2300,
    2600,
    'UM002',
    'Strona B',
    'Podstawa B',
    'Uwagi B',
    'Dodatkowe B',
  ],
];

async function get_table_headers() {
  try {
    const res = await fetch('/api/tables/headers');
    if (!res.ok) {
      throw new Error(`HTTP error! status: ${res.status}`);
    }
    return (await res.json()) as string[];
  } catch (err) {
    console.error('Error fetching table headers:', err);
    return null;
  }
}

function AddComents() {
  const [headers, setHeaders] = useState<string[] | null>(null);
  const [selectedRows, setSelectedRows] = useState<number[]>([]);

  useEffect(() => {
    (async () => {
      const data = await get_table_headers();
      setHeaders(data);
    })();
  }, []);

  const handleRowCheckboxChange = (rowIndex: number, checked: boolean) => {
    setSelectedRows((prev) => {
      const set = new Set(prev);
      if (checked) {
        set.add(rowIndex);
      } else {
        set.delete(rowIndex);
      }
      const arr = Array.from(set);

      // logujemy, które wiersze są wybrane
      console.log('Wybrane indeksy wierszy:', arr);
      console.log('Wybrane wiersze (dane):', arr.map((i) => rows[i]));

      return arr;
    });
  };

  if (!headers) {
    return <div>Ładowanie nagłówków tabeli...</div>;
  }

  return (
    <div>
  
     <div className="flex flex-col justify-end items-end w-[75vw]">
        <Button variant="default" className="h-[3.5vh] w-[7vw]">
            Wygneruj Pdf
        </Button>
      </div>

      <div className="overflow-x-auto overflow-y-auto max-h-[60vh] max-w-[75vw]">
      <Table className="min-w-max w-full">
        <TableHeader className="bg-gray-100 sticky top-0 z-10">
          <TableRow>
            {/* kolumna na checkboxy */}
            <TableHead className="w-10 px-2 py-2 text-center border-x border-y" />
            {headers.map((header, j) => (
              <TableHead
                key={j}
                className="px-2 py-2 text-left font-bold text-gray-800 border-x border-y"
              >
                {header}
              </TableHead>
            ))}
          </TableRow>
        </TableHeader>
        <TableBody>
          {rows.map((row, r) => (
            <TableRow key={r} className="hover:bg-gray-50">
              {/* checkbox na początku wiersza */}
              <TableCell className="px-2 py-2 text-center border-x border-y">
                <Checkbox
                  checked={selectedRows.includes(r)}
                  onCheckedChange={(value) =>
                    handleRowCheckboxChange(r, value === true)
                  }
                />
              </TableCell>

              {row.map((ele, e) => (
                <TableCell
                  key={e}
                  className={`px-4 py-2 text-left border-x border-y ${
                    e === 0 ? 'pl-4' : ''
                  }`}
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

export default AddComents;
