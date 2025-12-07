import { useEffect, useState } from 'react';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';
import { Button } from '@/components/ui/button';
import { Checkbox } from '@/components/ui/checkbox';
import DialogAddComment from './DialogAddComent';

interface SelectValue {
  id: number;
  value: string;
}

interface TaskBudget {
  id: number;
  value: string;
  type: string;
  description: string;
}

interface RowData {
  budget_part: string | null;
  funding_source: string | null;
  budget_amount: string | null;
  task_name: string | null;
  task_justification: string | null;
  expenditure_purpose: string | null;
  notes: string | null;
  additionals: string | null;
  division: SelectValue | null;
  chapter: SelectValue | null;
  paragraph: SelectValue | null;
  expense_group: { id: number; definition: string } | null;
  task_budget_full: TaskBudget | null;
  task_budget_function: TaskBudget | null;
  financial_needs_0: string | null;
  expenditure_limit_0: string | null;
  unallocated_task_funds_0: string | null;
  contract_amount_0: string | null;
  contract_number_0: string | null;
  [key: string]: any;
}

interface Row {
  id: number;
  row_datas: RowData[];
}

interface DepartmentTable {
  id: number;
  rows: Row[];
}

interface BudgetData {
  id: number;
  department_tables: DepartmentTable[];
}

type RowValues = string[];

const extractRowData = (data: Row): RowValues[] => {
  const getVal = (obj: any, key: string, nestedKey?: string) => {
    if (!obj) return null;
    if (nestedKey) return obj[key]?.[nestedKey] ?? null;
    return obj[key] ?? null;
  };

  return data.row_datas.map((r) => {
    const rowData: RowValues = [
      getVal(r, 'budget_part'),
      getVal(r, 'division', 'value'),
      getVal(r, 'chapter', 'value'),
      getVal(r, 'paragraph', 'value'),
      getVal(r, 'funding_source'),
      getVal(r, 'expense_group', 'definition'),
      getVal(r, 'task_budget_full', 'value'),
      getVal(r, 'task_budget_function', 'value'),
      getVal(r, 'program_project_name'),
      getVal(r, 'organizational_unit_name'),
      getVal(r, 'plan_wi'),
      getVal(r, 'fund_distributor'),
      getVal(r, 'budget_code'),
      getVal(r, 'task_name'),
      getVal(r, 'task_justification'),
      getVal(r, 'expenditure_purpose'),
      getVal(r, 'financial_needs_0'),
      getVal(r, 'expenditure_limit_0'),
      getVal(r, 'unallocated_task_funds_0'),
      getVal(r
        , 'contract_amount_0'),
      getVal(r, 'contract_number_0'),
      getVal(r, 'financial_needs_1'),
      getVal(r, 'expenditure_limit_1'),
      getVal(r, 'unallocated_task_funds_1'),
      getVal(r, 'contract_amount_1'),
      getVal(r, 'contract_number_1'),
      getVal(r, 'financial_needs_2'),
      getVal(r, 'expenditure_limit_2'),
      getVal(r, 'unallocated_task_funds_2'),
      getVal(r, 'contract_amount_2'),
      getVal(r, 'contract_number_2'),
      getVal(r, 'financial_needs_3'),
      getVal(r, 'expenditure_limit_3'),
      getVal(r, 'unallocated_task_funds_3'),
      getVal(r, 'contract_amount_3'),
      getVal(r, 'contract_number_3'),
      getVal(r, 'subsidy_agreement_party'),
      getVal(r, 'legal_basis_for_subsidy'),
      getVal(r, 'notes'),
      getVal(r, 'additionals'),
    ];

    return rowData.map((item) =>
      item === null || item === undefined ? '' : String(item),
    );
  });
};

async function get_table_headers(): Promise<string[] | null> {
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

async function get_table_data(tableId: number): Promise<RowValues[]> {
  try {
    const res = await fetch(`/api/tables/${tableId}`);
    if (!res.ok) {
      throw new Error(`HTTP error! status: ${res.status}`);
    }
    const data: BudgetData = await res.json();
    const processedRows: RowValues[] =
      data.department_tables.flatMap((departmentTable) =>
        departmentTable.rows.flatMap((row) => extractRowData(row)),
      );

    return processedRows;
  } catch (err) {
    console.error('Error fetching table data:', err);
    return [];
  }
}

function AddComents() {
  const [headers, setHeaders] = useState<string[] | null>(null);
  const [selectedRows, setSelectedRows] = useState<number[]>([]);
  const [tableRows, setTableRows] = useState<RowValues[]>([]);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [loading, setLoading] = useState<boolean>(true);

  const handleRowCheckboxChange = (rowIndex: number, checked: boolean) => {
    setSelectedRows((prev) => {
      const set = new Set(prev);
      if (checked) {
        set.add(rowIndex);
      } else {
        set.delete(rowIndex);
      }

      const arr = Array.from(set);
      console.log('Wybrane indeksy wierszy:', arr);
      console.log('Wybrane wiersze:', arr.map((i) => tableRows[i]));

      return arr;
    });
  };

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        const [headerData, rowData] = await Promise.all([
          get_table_headers(),
          get_table_data(1),
        ]);

        setHeaders(headerData);
        setTableRows(rowData);
      } catch (error) {
        console.error('Błąd ładowania danych budżetu:', error);
        setHeaders(null);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading || !headers) {
    return <div>Ładowanie danych tabeli...</div>;
  }

  if (tableRows.length === 0) {
    return <div>Brak danych do wyświetlenia.</div>;
  }

  const selectedRowsData = selectedRows.map((i) => tableRows[i]);

  return (
    <div>
      <div className="flex flex-col justify-end items-end w-[75vw]">
        <Button
          className="h-[3.5vh] w-[7vw]"
          onClick={() => setDialogOpen(true)}
        >
          Wygeneruj PDF
        </Button>
      </div>

      <div className="overflow-x-auto overflow-y-auto max-h-[60vh] max-w-[75vw] mt-[4vh]">
        <Table className="min-w-max w-full">
          <TableHeader className="bg-gray-100 sticky top-0 z-10">
            <TableRow>
              <TableHead className="w-10 px-2 py-2 text-center border-x border-y" />
              {headers.map((header, j) => (
                <TableHead
                  key={j}
                  className="px-2 py-2 text-left font-bold border-x border-y"
                >
                  {header}
                </TableHead>
              ))}
            </TableRow>
          </TableHeader>

          <TableBody>
            {tableRows.map((row, r) => (
              <TableRow key={r} className="hover:bg-gray-50">
                <TableCell className="px-2 py-2 text-center border-x border-y">
                  <Checkbox
                    checked={selectedRows.includes(r)}
                    onCheckedChange={(v) =>
                      handleRowCheckboxChange(r, v === true)
                    }
                  />
                </TableCell>

                {row.map((ele, e) => (
                  <TableCell
                    key={e}
                    className="px-4 py-2 text-left border-x border-y"
                  >
                    {ele}
                  </TableCell>
                ))}
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>

      {dialogOpen && (
        <DialogAddComment
          open={dialogOpen}
          onOpenChange={setDialogOpen}
          headers={headers}
          rows={selectedRowsData}
        />
      )}
    </div>
  );
}

export default AddComents;
