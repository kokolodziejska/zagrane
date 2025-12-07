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
    ['Dział A', '50000', '48000'],
    ['Dział B', '70000', '68000'],
    ['Dział C', '30000', '32000', ''], // nadmiarowy element zostanie obcięty
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

function DepartmentSetDate() {
  return (
    <div className="space-y-6">
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
                  {row
                    .slice(0, tab.headers.length)
                    .map((ele, e) => (
                      <TableCell
                        key={e}
                        className={`px-4 py-2 text-left border-x border-y ${
                          e === 0 ? 'pl-4 font-medium' : 'text-center'
                        }`}
                        style={{
                          width: e === 0 ? '5vw' : '15vw',
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
