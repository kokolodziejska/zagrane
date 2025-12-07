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

type RowValues = string[];

interface EnrichedRow {
    rowId: number | null;
    versionDate: string | null;
    lastUserId: number | null;
    lastUpdate: string | null;
    values: RowValues;
}

interface RowData {
    row_id?: number;
    version_date?: string;
    last_user_id?: number;
    last_update?: string;
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

interface DisplayRow {
    row: EnrichedRow;
    history: EnrichedRow[];
}

const extractRowData = (data: Row): EnrichedRow[] => {
    const getVal = (obj: any, key: string, nestedKey?: string) => {
        if (!obj) return null;
        if (nestedKey) return obj[key]?.[nestedKey] ?? null;
        return obj[key] ?? null;
    };

    return data.row_datas.map(r => {
        const rowData: (string | number | null)[] = [
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
            getVal(r, 'contract_amount_0'),
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

        const values = rowData.map(v => (v == null ? '' : String(v)));

        return {
            rowId: r.row_id ?? null,
            versionDate: r.version_date ?? null,
            lastUserId: r.last_user_id ?? null,
            lastUpdate: r.last_update ?? null,
            values,
        };
    });
};

async function get_table_headers(): Promise<string[] | null> {
    try {
        const res = await fetch('/api/tables/headers');
        if (!res.ok) return null;
        return (await res.json()) as string[];
    } catch {
        return null;
    }
}

async function get_table_data(tableId: number): Promise<EnrichedRow[]> {
    try {
        const res = await fetch(`/api/tables/${tableId}`);
        if (!res.ok) return [];
        const data: BudgetData = await res.json();
        return data.department_tables.flatMap(t =>
            t.rows.flatMap(r => extractRowData(r))
        );
    } catch {
        return [];
    }
}

function MangeBudget() {
    const TABLE_ID = 1;

    const [headers, setHeaders] = useState<string[] | null>(null);
    const [tableRows, setTableRows] = useState<EnrichedRow[]>([]);
    const [loading, setLoading] = useState(true);

    const [historyModalOpen, setHistoryModalOpen] = useState(false);
    const [historyRows, setHistoryRows] = useState<EnrichedRow[]>([]);

    const [editingCell, setEditingCell] = useState<{
        rowIndex: number;
        colIndex: number;
    } | null>(null);

    const handleCellChange = (targetRow: EnrichedRow, colIndex: number, newValue: string) => {
        setTableRows(prev =>
            prev.map(r => {
                if (r === targetRow) {
                    const updatedValues = [...r.values];
                    updatedValues[colIndex] = newValue;
                    return { ...r, values: updatedValues };
                }
                return r;
            })
        );
    };

    const formatLastUpdate = (iso: string | null): string => {
        if (!iso) return '';
        const d = new Date(iso);
        if (isNaN(d.getTime())) return '';
        const pad = (n: number) => n.toString().padStart(2, '0');
        const hh = pad(d.getHours());
        const mm = pad(d.getMinutes());
        const dd = pad(d.getDate());
        const MM = pad(d.getMonth() + 1);
        const yyyy = d.getFullYear();
        return `${hh}:${mm} ${dd}-${MM}-${yyyy}`;
    };

    useEffect(() => {
        const fetchData = async () => {
            setLoading(true);
            const [h, rows] = await Promise.all([
                get_table_headers(),
                get_table_data(TABLE_ID)
            ]);
            setHeaders(h);
            setTableRows(rows);
            setLoading(false);
        };
        fetchData();
    }, []);

    if (loading || !headers) return <div>Ładowanie danych...</div>;
    if (tableRows.length === 0) return <div>Brak danych</div>;

    const displayRows: DisplayRow[] = (() => {
        const groups = new Map<string, EnrichedRow[]>();
        let uniqueCounter = 0;

        for (const r of tableRows) {
            const key = r.rowId != null ? `id_${r.rowId}` : `u_${uniqueCounter++}`;
            const arr = groups.get(key);
            if (arr) arr.push(r);
            else groups.set(key, [r]);
        }

        const out: DisplayRow[] = [];

        for (const [key, rows] of groups.entries()) {
            if (rows.length === 1 || key.startsWith('u_')) {
                out.push({ row: rows[0], history: [] });
            } else {
                const sorted = [...rows].sort((a, b) => {
                    if (!a.versionDate && !b.versionDate) return 0;
                    if (!a.versionDate) return 1;
                    if (!b.versionDate) return -1;
                    return new Date(b.versionDate).getTime() - new Date(a.versionDate).getTime();
                });

                const latest = sorted[0];
                const history = sorted.slice(1);
                out.push({ row: latest, history });
            }
        }

        return out;
    })();

    const openHistory = (rows: EnrichedRow[]) => {
        if (!rows || rows.length === 0) return;
        setHistoryRows(rows);
        setHistoryModalOpen(true);
    };

    const closeHistory = () => {
        setHistoryModalOpen(false);
        setHistoryRows([]);
    };

    return (
        <div>
            <div className="flex flex-col justify-end items-end w-[80vw]">
                <Button className="h-[3.5vh] w-[7vw]">
                    Wygneruj Excel
                </Button>
            </div>

            <div className="overflow-x-auto overflow-y-auto max-h-[60vh] max-w-[80vw] mt-[4vh]">
                <Table className="min-w-max w-full">
                    <TableHeader className="bg-gray-100 sticky top-0 z-10">
                        <TableRow>
                            <TableHead className="w-8 px-1 py-2 border-x border-y whitespace-normal break-words"></TableHead>
                            {headers.map((h, i) => (
                                <TableHead
                                    key={i}
                                    className="px-2 py-2 text-left font-bold text-gray-800 border-x border-y max-w-60 whitespace-normal break-words"
                                >
                                    {h}
                                </TableHead>
                            ))}
                        </TableRow>
                    </TableHeader>

                    <TableBody>
                        {displayRows.map(({ row, history }, rowIndex) => (
                            <TableRow
                                key={rowIndex}
                                className="hover:bg-gray-50"
                            >
                                <TableCell className="px-1 py-1 text-center border-x border-y align-middle whitespace-normal break-words">
                                    {history.length > 0 && (
                                        <button
                                            type="button"
                                            onClick={() => openHistory(history)}
                                            className="h-6 w-6 rounded-full bg-blue-600 text-white text-xs font-bold flex items-center justify-center hover:bg-blue-700"
                                            aria-label="Historia zmian"
                                        >
                                            H
                                        </button>
                                    )}
                                </TableCell>
                                {row.values.map((v, colIndex) => {
                                    const isEditing =
                                        editingCell &&
                                        editingCell.rowIndex === rowIndex &&
                                        editingCell.colIndex === colIndex;

                                    return (
                                        <TableCell
                                            key={colIndex}
                                            className="px-2 py-1 text-left border-x border-y max-w-60 whitespace-normal break-words align-top"
                                            onClick={() => {
                                                if (!isEditing) {
                                                    setEditingCell({ rowIndex, colIndex });
                                                }
                                            }}
                                        >
                                            {isEditing ? (
                                                <input
                                                    type="text"
                                                    value={v}
                                                    autoFocus
                                                    onClick={e => e.stopPropagation()}
                                                    onChange={e =>
                                                        handleCellChange(row, colIndex, e.target.value)
                                                    }
                                                    onBlur={() => setEditingCell(null)}
                                                    onKeyDown={e => {
                                                        if (e.key === 'Enter') {
                                                            setEditingCell(null);
                                                        }
                                                    }}
                                                    className="w-full p-0 m-0 bg-white border border-gray-300 rounded-sm focus:outline-none focus:ring-1 focus:ring-blue-500 text-sm"
                                                />
                                            ) : (
                                                <span className="block w-full whitespace-normal break-words text-sm">
                                                    {v}
                                                </span>
                                            )}
                                        </TableCell>
                                    );
                                })}
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </div>

            {historyModalOpen && (
                <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40">
                    <div className="bg-white rounded-lg shadow-lg max-w-[95vw] max-h-[85vh] w-[90vw] p-6 flex flex-col">
                        <div className="flex justify-between items-center mb-4">
                            <h2 className="text-lg font-semibold">Historia zmian</h2>
                            <button
                                type="button"
                                onClick={closeHistory}
                                className="px-3 py-1 text-sm rounded-md bg-gray-200 hover:bg-gray-300"
                            >
                                Zamknij
                            </button>
                        </div>
                        <div className="overflow-auto border rounded">
                            <Table className="min-w-max w-full">
                                <TableHeader>
                                    <TableRow>
                                        <TableHead className="px-2 py-2 text-left font-bold text-gray-800 border-x border-y max-w-40 whitespace-normal break-words">
                                            Użytkownik
                                        </TableHead>
                                        <TableHead className="px-2 py-2 text-left font-bold text-gray-800 border-x border-y max-w-40 whitespace-normal break-words">
                                            Ostatnia edycja
                                        </TableHead>
                                        {headers.map((h, i) => (
                                            <TableHead
                                                key={i}
                                                className="px-2 py-2 text-left font-bold text-gray-800 border-x border-y max-w-60 whitespace-normal break-words"
                                            >
                                                {h}
                                            </TableHead>
                                        ))}
                                    </TableRow>
                                </TableHeader>
                                <TableBody>
                                    {historyRows.map((hr, idx) => (
                                        <TableRow key={idx} className="hover:bg-gray-50">
                                            <TableCell className="px-2 py-1 text-left border-x border-y max-w-40 whitespace-normal break-words">
                                                {hr.lastUserId != null ? String(hr.lastUserId) : ''}
                                            </TableCell>
                                            <TableCell className="px-2 py-1 text-left border-x border-y max-w-40 whitespace-normal break-words">
                                                {formatLastUpdate(hr.lastUpdate)}
                                            </TableCell>
                                            {hr.values.map((v, j) => (
                                                <TableCell
                                                    key={j}
                                                    className="px-2 py-1 text-left border-x border-y max-w-60 whitespace-normal break-words"
                                                >
                                                    {v}
                                                </TableCell>
                                            ))}
                                        </TableRow>
                                    ))}
                                </TableBody>
                            </Table>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}

export default MangeBudget;
