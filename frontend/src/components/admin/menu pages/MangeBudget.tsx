import { useEffect, useState } from 'react';
import { useSelector } from 'react-redux';
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from '@/components/ui/table';
import { Button } from '@/components/ui/button';
import SelectDivision from '@/components/admin/SelectDivision';

type Division = {
    id: number;
    value: string;
};

type Chapter = {
    id: number;
    value: string;
};

type Paragraph = {
    id: number;
    value: string;
    expense_group: {
        id: number;
        definition: string;
    };
};

type RowValues = string[];

interface EnrichedRow {
    tableId: number;
    departmentTableId: number | null;
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
    year: number;
    version: string;
    isOpen: boolean;
    budget: number;
    department_tables: DepartmentTable[];
}

interface DisplayRow {
    row: EnrichedRow;
    history: EnrichedRow[];
}

interface ChangeRecord {
    tableId: number;
    departmentTableId: number | null;
    rowId: number | null;
    isDeleted: boolean;
    values: RowValues;
    lastUserId: number | null;
    lastUpdate: string;
}

const twoDigitRegex = /^\d{2}$/;
const threeDigitRegex = /^\d{3}$/;
const fourDigitRegex = /^\d{4}$/;
const fiveDigitRegex = /^\d{5}$/;
const oneDigitRegex = /^\d$/;
const fullTaskRegex = /^\d{2}\.\d{2}\.\d{2}\.\d{2}$/;
const funcTaskRegex = /^\d{2}\.\d{2}$/;
const amountRegex = /^\d+([.,]\d{1,2})?$/;

const columnRegexes: (RegExp | null)[] = [
    twoDigitRegex,    // 0 - Część budżetowa
    threeDigitRegex,  // 1 - Dział
    fiveDigitRegex,   // 2 - Rozdział
    threeDigitRegex,  // 3 - Paragraf
    oneDigitRegex,    // 4 - Źródło finansowania
    null,             // 5 - Grupa wydatków (auto)
    fullTaskRegex,    // 6 - Budżet zadaniowy w pełnej szczegółowości
    funcTaskRegex,    // 7 - Budżet zadaniowy (nr funkcji, nr zadania)
    null,             // 8 - Nazwa programu/projektu
    null,             // 9 - Nazwa komórki organizacyjnej
    null,             // 10 - Plan WI
    null,             // 11 - Dysponent środków
    null,             // 12 - Budżet (tekst/kwota - brak regex teraz)
    null,             // 13 - Nazwa zadania
    null,             // 14 - Szczegółowe uzasadnienie
    null,             // 15 - Przeznaczenie wydatków
    amountRegex,      // 16 - Potrzeby finansowe
    amountRegex,      // 17 - Limit wydatków
    amountRegex,      // 18 - Kwota niezabezpieczona
    amountRegex,      // 19 - Kwota zawartej umowy
    null,             // 20 - Nr umowy
    amountRegex,      // 21 - Potrzeby finansowe 2 (jeśli masz kolejne lata)
    amountRegex,      // 22 - Limit wydatków 2
    amountRegex,      // 23 - Kwota niezabezpieczona 2
    amountRegex,      // 24 - Kwota zawartej umowy 2
    null,             // 25 - Nr umowy 2
    amountRegex,      // 26 - Potrzeby finansowe 3
    amountRegex,      // 27 - Limit wydatków 3
    amountRegex,      // 28 - Kwota niezabezpieczona 3
    amountRegex,      // 29 - Kwota zawartej umowy 3
    null,             // 30 - Nr umowy 3
    amountRegex,      // 31 - Potrzeby finansowe 4
    amountRegex,      // 32 - Limit wydatków 4
    amountRegex,      // 33 - Kwota niezabezpieczona 4
    amountRegex,      // 34 - Kwota zawartej umowy 4
    null,             // 35 - Nr umowy 4
    null,             // 36 - W przypadku dotacji - z kim
    null,             // 37 - Podstawa prawna
    null,             // 38 - Uwagi
    null,             // 39 - Dodatkowe
];

const extractRowData = (
    data: Row,
    tableId: number,
    departmentTableId: number
): EnrichedRow[] => {
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
            tableId,
            departmentTableId,
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
        const effectiveTableId = data.id ?? tableId;
        return data.department_tables.flatMap(t =>
            t.rows.flatMap(r => extractRowData(r, effectiveTableId, t.id))
        );
    } catch {
        return [];
    }
}

async function get_divisions(): Promise<Division[]> {
    try {
        const res = await fetch('/api/divisions/');
        if (!res.ok) return [];
        return (await res.json()) as Division[];
    } catch {
        return [];
    }
}

async function get_chapters(divisionValue: string): Promise<Chapter[]> {
    if (!divisionValue) return [];
    try {
        const res = await fetch(`/api/divisions/${divisionValue}/chapters`);
        if (!res.ok) return [];
        return (await res.json()) as Chapter[];
    } catch {
        return [];
    }
}

async function get_paragraphs(chapterValue: string): Promise<Paragraph[]> {
    if (!chapterValue) return [];
    try {
        const res = await fetch(`/api/chapters/${chapterValue}/paragraphs`);
        if (!res.ok) return [];
        return (await res.json()) as Paragraph[];
    } catch {
        return [];
    }
}

const upsertChange = (
    prev: ChangeRecord[],
    updatedRow: EnrichedRow,
    isDeleted: boolean,
    userId: number | null
): ChangeRecord[] => {
    const lastUpdate = new Date().toISOString();

    const newRecord: ChangeRecord = {
        tableId: updatedRow.tableId,
        departmentTableId: updatedRow.departmentTableId,
        rowId: updatedRow.rowId,
        isDeleted,
        values: updatedRow.values,
        lastUserId: userId,
        lastUpdate,
    };

    const idx = prev.findIndex(
        c =>
            c.tableId === updatedRow.tableId &&
            c.departmentTableId === updatedRow.departmentTableId &&
            c.rowId === updatedRow.rowId
    );

    if (idx === -1) {
        return [...prev, newRecord];
    }

    const copy = [...prev];
    copy[idx] = newRecord;
    return copy;
};

const validateCellValue = (colIndex: number, value: string): boolean => {
    const regex = columnRegexes[colIndex];
    if (!regex) return true;
    const trimmed = value.trim();
    if (trimmed === '') return true;
    return regex.test(trimmed);
};

function MangeBudget() {
    const TABLE_ID = 1;

    const [headers, setHeaders] = useState<string[] | null>(null);
    const [tableRows, setTableRows] = useState<EnrichedRow[]>([]);
    const [loading, setLoading] = useState(true);

    const [divisions, setDivisions] = useState<Division[]>([]);
    const [divisionsLoading, setDivisionsLoading] = useState(false);

    const [chapters, setChapters] = useState<Record<string, Chapter[]>>({});
    const [chaptersLoading, setChaptersLoading] = useState<Record<string, boolean>>({});

    const [paragraphs, setParagraphs] = useState<Record<string, Paragraph[]>>({});
    const [paragraphsLoading, setParagraphsLoading] = useState<Record<string, boolean>>({});

    const [historyModalOpen, setHistoryModalOpen] = useState(false);
    const [historyRows, setHistoryRows] = useState<EnrichedRow[]>([]);

    const [editingCell, setEditingCell] = useState<{
        rowIndex: number;
        colIndex: number;
    } | null>(null);

    const [deleteModalOpen, setDeleteModalOpen] = useState(false);
    const [rowToDelete, setRowToDelete] = useState<EnrichedRow | null>(null);

    const [changedRows, setChangedRows] = useState<ChangeRecord[]>([]);

    const currentUserId = useSelector((state: any) => state.user?.userId ?? null);

    const loadChapters = async (divisionValue: string) => {
        if (!divisionValue) return;
        setChaptersLoading(prev => ({ ...prev, [divisionValue]: true }));
        const data = await get_chapters(divisionValue);
        setChapters(prev => ({ ...prev, [divisionValue]: data }));
        setChaptersLoading(prev => ({ ...prev, [divisionValue]: false }));
    };

    const loadParagraphs = async (chapterValue: string) => {
        if (!chapterValue) return;
        setParagraphsLoading(prev => ({ ...prev, [chapterValue]: true }));
        const data = await get_paragraphs(chapterValue);
        setParagraphs(prev => ({ ...prev, [chapterValue]: data }));
        setParagraphsLoading(prev => ({ ...prev, [chapterValue]: false }));
    };

    const handleCellChange = (
        targetRow: EnrichedRow,
        colIndex: number,
        newValue: string
    ) => {
        setTableRows(prev =>
            prev.map(r => {
                if (r !== targetRow) return r;
                const updatedValues = [...r.values];
                updatedValues[colIndex] = newValue;
                return { ...r, values: updatedValues };
            })
        );
    };

    const handleCellBlur = (row: EnrichedRow) => {
        setChangedRows(prevChanges => upsertChange(prevChanges, row, false, currentUserId));
    };

    const handleDivisionChange = (targetRow: EnrichedRow, newDivision: string) => {
        const updatedValues = [...targetRow.values];
        updatedValues[1] = newDivision;
        updatedValues[2] = '';
        updatedValues[3] = '';
        updatedValues[5] = '';

        const updatedRow: EnrichedRow = {
            ...targetRow,
            values: updatedValues,
        };

        setTableRows(prev =>
            prev.map(r => (r === targetRow ? updatedRow : r))
        );

        setChangedRows(prevChanges => upsertChange(prevChanges, updatedRow, false, currentUserId));

        if (newDivision) {
            loadChapters(newDivision);
        }
    };

    const handleChapterChange = (targetRow: EnrichedRow, newChapter: string) => {
        const updatedValues = [...targetRow.values];
        updatedValues[2] = newChapter;
        updatedValues[3] = '';
        updatedValues[5] = '';

        const updatedRow: EnrichedRow = {
            ...targetRow,
            values: updatedValues,
        };

        setTableRows(prev =>
            prev.map(r => (r === targetRow ? updatedRow : r))
        );

        setChangedRows(prevChanges => upsertChange(prevChanges, updatedRow, false, currentUserId));

        if (newChapter) {
            loadParagraphs(newChapter);
        }
    };

    const handleParagraphChange = (targetRow: EnrichedRow, newParagraph: string) => {
        const chapterValue = targetRow.values[2];
        if (!chapterValue) {
            return;
        }

        const chapterParagraphs = paragraphs[chapterValue] ?? [];
        const paragraphObj = chapterParagraphs.find(p => p.value === newParagraph);
        const expenseDefinition = paragraphObj?.expense_group?.definition ?? '';

        const updatedValues = [...targetRow.values];
        updatedValues[3] = newParagraph;
        updatedValues[5] = expenseDefinition;

        const updatedRow: EnrichedRow = {
            ...targetRow,
            values: updatedValues,
        };

        setTableRows(prev =>
            prev.map(r => (r === targetRow ? updatedRow : r))
        );

        setChangedRows(prevChanges => upsertChange(prevChanges, updatedRow, false, currentUserId));
    };

    const handleAskDeleteRow = (targetRow: EnrichedRow) => {
        setRowToDelete(targetRow);
        setDeleteModalOpen(true);
    };

    const handleConfirmDelete = () => {
        if (!rowToDelete) return;

        const rowCopy = rowToDelete;

        setTableRows(prev => prev.filter(r => r !== rowCopy));

        setChangedRows(prevChanges =>
            upsertChange(prevChanges, rowCopy, true, currentUserId)
        );

        setRowToDelete(null);
        setDeleteModalOpen(false);
    };

    const handleCancelDelete = () => {
        setRowToDelete(null);
        setDeleteModalOpen(false);
    };

    const handleAddRow = () => {
        if (!headers) return;
        const emptyValues: RowValues = Array(headers.length).fill('');
        const defaultDepartmentTableId =
            tableRows.length > 0 ? tableRows[0].departmentTableId : null;
        const defaultTableId =
            tableRows.length > 0 ? tableRows[0].tableId : TABLE_ID;
        const newRow: EnrichedRow = {
            tableId: defaultTableId,
            departmentTableId: defaultDepartmentTableId,
            rowId: null,
            versionDate: null,
            lastUserId: null,
            lastUpdate: null,
            values: emptyValues,
        };
        setTableRows(prev => [...prev, newRow]);
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
        const fetchAll = async () => {
            setLoading(true);
            setDivisionsLoading(true);
            const [h, rows, divs] = await Promise.all([
                get_table_headers(),
                get_table_data(TABLE_ID),
                get_divisions(),
            ]);
            setHeaders(h);
            setTableRows(rows);
            setDivisions(divs);
            setLoading(false);
            setDivisionsLoading(false);

            const uniqueDivisions = Array.from(
                new Set(
                    rows
                        .map(r => r.values[1])
                        .filter(v => v && v.trim().length > 0)
                )
            ) as string[];
            uniqueDivisions.forEach(d => {
                loadChapters(d);
            });

            const uniqueChapters = Array.from(
                new Set(
                    rows
                        .map(r => r.values[2])
                        .filter(v => v && v.trim().length > 0)
                )
            ) as string[];
            uniqueChapters.forEach(ch => {
                loadParagraphs(ch);
            });
        };
        fetchAll();
    }, []);

    // global walidacja – jeśli jakakolwiek komórka jest niepoprawna,
    // przycisk "Zapisz zmiany" będzie zablokowany
    const hasInvalidCells = tableRows.some(row =>
        row.values.some((v, colIndex) => !validateCellValue(colIndex, v))
    );

    const handleGenerateExcel = () => {
        // bierzemy główne ID tabeli – albo z pierwszego wiersza, albo fallback na stałą
        const mainTableId =
            tableRows.length > 0 ? tableRows[0].tableId : TABLE_ID;

        const url = `http://localhost:8000/api/tables/${mainTableId}/generate_spreadsheet`;

        // najprostsze podejście – przeglądarka sama obsłuży pobranie
        window.open(url, '_blank');
    };


    const handleSaveChanges = async () => {
        // możesz zostawić loga do debugowania
        console.log('Kliknięto Zapisz zmiany', changedRows);

        // budujemy dokładnie taki payload, jak w przykładzie
        const payload = changedRows.map(cr => ({
            tableId: cr.tableId,
            departmentTableId: cr.departmentTableId,
            rowId: cr.rowId,
            isDeleted: cr.isDeleted,
            values: cr.values,
            lastUserId: cr.lastUserId,
            lastUpdate: cr.lastUpdate,
        }));

        try {
            const res = await fetch('http://localhost:8000/api/tables/batch-update', {
                method: 'POST',
                credentials: 'include',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(payload),
            });

            if (!res.ok) {
                console.error('Błąd zapisu zmian', await res.text());
                return;
            }

            // po wysłaniu czyścimy tabelę zmian
            setChangedRows([]);
            console.log('Zapis zmian OK');
        } catch (e) {
            console.error('Błąd zapisu zmian', e);
        }
    };


    if (loading || !headers) return <div>Ładowanie danych...</div>;
    if (tableRows.length === 0)
        return (
            <div>
                Brak danych
                <div className="mt-4">
                    <Button
                        className="bg-blue-600 hover:bg-blue-700 text-white rounded-full h-10 w-10 p-0 text-xl"
                        onClick={handleAddRow}
                    >
                        +
                    </Button>
                </div>
            </div>
        );

    const displayRows: DisplayRow[] = (() => {
        const groups = new Map<string, EnrichedRow[]>();
        let uniqueCounter = 0;

        for (const r of tableRows) {
            const key =
                r.rowId != null ? `id_${r.rowId}` : `u_${uniqueCounter++}`;
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
                    return (
                        new Date(b.versionDate).getTime() -
                        new Date(a.versionDate).getTime()
                    );
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
                <div className="flex gap-2">
                    <Button
                        className="h-[3.5vh] w-[10vw]"
                        onClick={handleSaveChanges}
                    >
                        Zapisz zmiany
                    </Button>
                    <Button className="h-[3.5vh] w-[7vw]">
                        Wygneruj Excel
                    </Button>
                </div>
            </div>

            <div className="overflow-x-auto overflow-y-auto max-h-[60vh] max-w-[80vw] mt-[4vh]">
                <Table className="min-w-max w-full">
                    <TableHeader className="bg-gray-100 sticky top-0 z-10">
                        <TableRow>
                            <TableHead className="w-8 px-1 py-2 border-x border-y whitespace-normal break-words" />
                            <TableHead className="w-8 px-1 py-2 border-x border-y whitespace-normal break-words" />
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
                        {displayRows.map(({ row, history }, displayRowIndex) => (
                            <TableRow
                                key={displayRowIndex}
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

                                <TableCell className="px-1 py-1 text-center border-x border-y align-middle whitespace-normal break-words">
                                    <button
                                        type="button"
                                        onClick={() => handleAskDeleteRow(row)}
                                        className="h-6 w-6 rounded-full bg-red-600 text-white text-xs font-bold flex items-center justify-center hover:bg-red-700"
                                        aria-label="Usuń wiersz"
                                    >
                                        -
                                    </button>
                                </TableCell>

                                {row.values.map((v, colIndex) => {
                                    const invalid = !validateCellValue(colIndex, v);

                                    if (colIndex === 1) {
                                        return (
                                            <TableCell
                                                key={colIndex}
                                                className={`px-2 py-1 text-left border-x border-y max-w-60 whitespace-normal break-words align-top${
                                                    invalid ? ' bg-red-100 border-red-500' : ''
                                                }`}
                                                onClick={e => e.stopPropagation()}
                                            >
                                                <SelectDivision
                                                    value={v}
                                                    divisions={divisions}
                                                    loading={divisionsLoading}
                                                    onChange={newVal =>
                                                        handleDivisionChange(
                                                            row,
                                                            newVal
                                                        )
                                                    }
                                                />
                                            </TableCell>
                                        );
                                    }

                                    if (colIndex === 2) {
                                        const divisionValue = row.values[1];
                                        if (!divisionValue) {
                                            return (
                                                <TableCell
                                                    key={colIndex}
                                                    className={`px-2 py-1 text-left border-x border-y max-w-60 whitespace-normal break-words align-top${
                                                        invalid ? ' bg-red-100 border-red-500' : ''
                                                    }`}
                                                >
                                                    <span className="block w-full whitespace-normal break-words text-sm">
                                                        {v}
                                                    </span>
                                                </TableCell>
                                            );
                                        }

                                        const divisionChapters =
                                            chapters[divisionValue] ?? [];
                                        const isChapterLoading =
                                            chaptersLoading[divisionValue] ??
                                            false;

                                        return (
                                            <TableCell
                                                key={colIndex}
                                                className={`px-2 py-1 text-left border-x border-y max-w-60 whitespace-normal break-words align-top${
                                                    invalid ? ' bg-red-100 border-red-500' : ''
                                                }`}
                                                onClick={e => e.stopPropagation()}
                                            >
                                                <SelectDivision
                                                    value={v}
                                                    divisions={divisionChapters}
                                                    loading={isChapterLoading}
                                                    onChange={newVal =>
                                                        handleChapterChange(
                                                            row,
                                                            newVal
                                                        )
                                                    }
                                                />
                                            </TableCell>
                                        );
                                    }

                                    if (colIndex === 3) {
                                        const chapterValue = row.values[2];
                                        if (!chapterValue) {
                                            return (
                                                <TableCell
                                                    key={colIndex}
                                                    className={`px-2 py-1 text-left border-x border-y max-w-60 whitespace-normal break-words align-top${
                                                        invalid ? ' bg-red-100 border-red-500' : ''
                                                    }`}
                                                >
                                                    <span className="block w-full whitespace-normal break-words text-sm">
                                                        {v}
                                                    </span>
                                                </TableCell>
                                            );
                                        }

                                        const chapterParagraphs =
                                            paragraphs[chapterValue] ?? [];
                                        const isParagraphLoading =
                                            paragraphsLoading[chapterValue] ??
                                            false;

                                        const paragraphOptions = chapterParagraphs.map(p => ({
                                            id: p.id,
                                            value: p.value,
                                        }));

                                        return (
                                            <TableCell
                                                key={colIndex}
                                                className={`px-2 py-1 text-left border-x border-y max-w-60 whitespace-normal break-words align-top${
                                                    invalid ? ' bg-red-100 border-red-500' : ''
                                                }`}
                                                onClick={e => e.stopPropagation()}
                                            >
                                                <SelectDivision
                                                    value={v}
                                                    divisions={paragraphOptions}
                                                    loading={isParagraphLoading}
                                                    onChange={newVal =>
                                                        handleParagraphChange(
                                                            row,
                                                            newVal
                                                        )
                                                    }
                                                />
                                            </TableCell>
                                        );
                                    }

                                    if (colIndex === 5) {
                                        return (
                                            <TableCell
                                                key={colIndex}
                                                className={`px-2 py-1 text-left border-x border-y max-w-60 whitespace-normal break-words align-top${
                                                    invalid ? ' bg-red-100 border-red-500' : ''
                                                }`}
                                            >
                                                <span className="block w-full whitespace-normal break-words text-sm">
                                                    {v}
                                                </span>
                                            </TableCell>
                                        );
                                    }

                                    const isEditing =
                                        editingCell &&
                                        editingCell.rowIndex === displayRowIndex &&
                                        editingCell.colIndex === colIndex;

                                    return (
                                        <TableCell
                                            key={colIndex}
                                            className={`px-2 py-1 text-left border-x border-y max-w-60 whitespace-normal break-words align-top${
                                                invalid ? ' bg-red-100 border-red-500' : ''
                                            }`}
                                            onClick={() => {
                                                if (!isEditing) {
                                                    setEditingCell({
                                                        rowIndex: displayRowIndex,
                                                        colIndex,
                                                    });
                                                }
                                            }}
                                        >
                                            {isEditing ? (
                                                <input
                                                    type="text"
                                                    value={v}
                                                    autoFocus
                                                    onClick={e =>
                                                        e.stopPropagation()
                                                    }
                                                    onChange={e =>
                                                        handleCellChange(
                                                            row,
                                                            colIndex,
                                                            e.target.value
                                                        )
                                                    }
                                                    onBlur={() => {
                                                        handleCellBlur(row);
                                                        setEditingCell(null);
                                                    }}
                                                    onKeyDown={e => {
                                                        if (e.key === 'Enter') {
                                                            handleCellBlur(row);
                                                            setEditingCell(
                                                                null
                                                            );
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

            <div className="max-w-[80vw] mt-4 flex justify-start">
                <Button
                    className="bg-blue-600 hover:bg-blue-700 text-white rounded-full h-10 w-10 p-0 text-xl"
                    onClick={handleAddRow}
                >
                    +
                </Button>
            </div>

            {historyModalOpen && (
                <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40">
                    <div className="bg-white rounded-lg shadow-lg max-w-[95vw] max-h-[85vh] w-[90vw] p-6 flex flex-col">
                        <div className="flex justify-between items-center mb-4">
                            <h2 className="text-lg font-semibold">
                                Historia zmian
                            </h2>
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
                                        <TableRow
                                            key={idx}
                                            className="hover:bg-gray-50"
                                        >
                                            <TableCell className="px-2 py-1 text-left border-x border-y max-w-40 whitespace-normal break-words">
                                                {hr.lastUserId != null
                                                    ? String(hr.lastUserId)
                                                    : ''}
                                            </TableCell>
                                            <TableCell className="px-2 py-1 text-left border-x border-y max-w-40 whitespace-normal break-words">
                                                {formatLastUpdate(
                                                    hr.lastUpdate
                                                )}
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

            {deleteModalOpen && (
                <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40">
                    <div className="bg-white rounded-lg shadow-lg w-[400px] max-w-[90vw] p-6">
                        <h2 className="text-lg font-semibold mb-4">
                            Czy na pewno chcesz usunąć ten wiersz?
                        </h2>
                        <div className="flex justify-end gap-3">
                            <button
                                type="button"
                                onClick={handleCancelDelete}
                                className="px-4 py-2 text-sm rounded-md bg-gray-200 hover:bg-gray-300"
                            >
                                Anuluj
                            </button>
                            <button
                                type="button"
                                onClick={handleConfirmDelete}
                                className="px-4 py-2 text-sm rounded-md bg-red-600 text-white hover:bg-red-700"
                            >
                                Usuń
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}

export default MangeBudget;
