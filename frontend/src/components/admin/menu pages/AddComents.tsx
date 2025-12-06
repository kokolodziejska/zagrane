import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableFooter,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';
import type AddComentsPage from '@/pages/admin/dashboard/AddComentsPage';

const tab = {
  headers: [
    'Funkcja Zadania Budżetowego',
    'Nazwa Projektu Programu',
    'Nazwa Jednostki Organizacyjnej',
    'Plan WI',
    'Dystrybutor Funduszy',
    'Kwota Budżetu',
    'Nazwa Zadania',
    'Uzasadnienie Zadania',
    'Cel Wydatków',
    'Potrzeby Finansowe',
    'Limit Wydatków',
    'Nieużytkowane Fundusze Zadania',
    'Kwota Umowy',
    'Potrzeby Finansowe 1',
    'Limit Wydatków 1',
    'Nieużytkowane Fundusze Zadania 1',
    'Kwota Umowy 1',
    'Potrzeby Finansowe 2',
    'Limit Wydatków 2',
    'Nieużytkowane Fundusze Zadania 2',
    'Kwota Umowy 2',
    'Potrzeby Finansowe 3',
    'Limit Wydatków 3',
    'Nieużytkowane Fundusze Zadania 3',
    'Kwota Umowy 3',
    'Numer Umowy',
    'Strona Umowy Dotycząca Subwencji',
    'Podstawa Prawna Subwencji',
    'Uwagi',
    'Dodatkowe Informacje',
  ],
  rows: [
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
  ],
};

function AddComents() {
  return (
    <div className="overflow-x-auto overflow-y-auto max-h-[60vh] w-full">
      <Table className="min-w-max w-full">
        <TableHeader className="bg-gray-100 sticky top-0 z-10">
          <TableRow>
            {tab.headers.map((header, j) => (
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
          {tab.rows.map((row, r) => (
            <TableRow key={r} className="hover:bg-gray-50">
              {row.map((ele, e) => (
                <TableCell
                  key={e}
                  className={`px-4 py-2 text-left border-x border-y ${e === 0 ? 'pl-4' : ''}`}
                >
                  {ele}
                </TableCell>
              ))}
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
}

export default AddComents;
