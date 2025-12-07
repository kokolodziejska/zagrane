import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';

const tab = {
  headers: ['Dział', 'Data początkowa', 'Data końcowa'],
  rows: [
 
  ['Dział A', '11.12.2025', '20.12.2025'],
  ['Dział B', '05.01.2025', '18.01.2025'],
  ['Dział C', '12.02.2025', '25.02.2025'],
  ['Dział D', '03.03.2025', '15.03.2025'],
  ['Dział E', '21.03.2025', '30.03.2025'],
  ['Dział F', '10.04.2025', '22.04.2025'],
  ['Dział G', '01.05.2025', '15.05.2025'],
  ['Dział H', '17.05.2025', '31.05.2025'],
  ['Dział I', '04.06.2025', '18.06.2025'],
  ['Dział J', '20.06.2025', '05.07.2025'],
  ['Dział K', '11.07.2025', '25.07.2025'],
  ['Dział L', '02.08.2025', '17.08.2025'],
  ['Dział M', '19.08.2025', '01.09.2025'],
  ['Dział N', '05.09.2025', '18.09.2025'],
  ['Dział O', '20.09.2025', '05.10.2025']

  ],
};

function DepartmentSetDate() {
  return (
    <div >
      <div>
        <Table className="min-w-max w-full">
          <TableHeader className="bg-gray-100">
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

        <div className="overflow-x-auto overflow-y-auto max-h-[55vh] scrollbar-hide">
          <Table className="min-w-max w-full">
            <TableBody>
              {tab.rows.map((row, r) => (
                <TableRow key={r} className="hover:bg-gray-50">
                  {row
                    .slice(0, tab.headers.length)
                    .map((ele, e) => (
                      <TableCell
                        key={e}
                        className={`px-4 py-2 text-left border-x border-y ${
                          e === 0 ? 'pl-4 font-medium' : 'text-center'
                        }`}
                        style={{
                          width: e === 0 ? '7vw' : '15vw',
                        }}
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
    </div>
  );
}

export default DepartmentSetDate;
