import { useField } from 'formik';
import { Checkbox } from '@/components/ui/checkbox';

type ColumnOption = {
  id: number;
  label: string;
};

type Props = {
  name: string;              // nazwa pola w Formiku, np. "columns"
  options: ColumnOption[];   // lista kolumn (id + label)
};

function SelectColumns({ name, options }: Props) {
  const [field, , helpers] = useField<number[]>({ name });
  const selected = field.value || [];

  const isAllSelected = selected.length === options.length && options.length > 0;

  const toggleAll = (checked: boolean) => {
    if (checked) {
      helpers.setValue(options.map((o) => o.id)); // wszystkie id
    } else {
      helpers.setValue([]);
    }
  };

  const toggleOne = (id: number, checked: boolean) => {
    const set = new Set(selected);
    if (checked) {
      set.add(id);
    } else {
      set.delete(id);
    }
    helpers.setValue(Array.from(set).sort((a, b) => a - b));
  };

  return (
    <div className="border rounded-md p-2 max-w-[75vw]">
      <div className="flex items-center gap-2 mb-2">
        <Checkbox
          checked={isAllSelected}
          onCheckedChange={(v) => toggleAll(v === true)}
        />
        <span className="text-sm font-semibold">
          Wybierz kolumny do PDF
        </span>
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-2 max-h-[28vh] overflow-y-auto pr-1">
        {options.map((opt) => (
          <label
            key={opt.id}
            className="flex items-center gap-2 text-xs cursor-pointer"
          >
            <Checkbox
              checked={selected.includes(opt.id)}
              onCheckedChange={(v) => toggleOne(opt.id, v === true)}
            />
            <span className="truncate" title={opt.label}>
              {opt.label}
            </span>
          </label>
        ))}
      </div>
    </div>
  );
}

export default SelectColumns;
