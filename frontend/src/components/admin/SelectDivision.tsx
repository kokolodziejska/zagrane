import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectLabel,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';

export type Division = {
  id: number;
  value: string;
};

type Props = {
  value: string;
  divisions: Division[];
  loading?: boolean;
  onChange: (newValue: string) => void;
};

function SelectDivision({ value, divisions, loading, onChange }: Props) {
  const hasDivisions = divisions && divisions.length > 0;

  return (
    <Select value={value} onValueChange={onChange}>
      <SelectTrigger className="w-full min-w-[6rem] max-w-[8rem]">
        <SelectValue
          placeholder={
            loading
              ? 'Ładowanie działów...'
              : hasDivisions
              ? 'Wybierz dział'
              : 'Brak działów'
          }
        />
      </SelectTrigger>

      <SelectContent>
        <SelectGroup>
          <SelectLabel>Dział</SelectLabel>

          {!hasDivisions ? (
            <div className="px-2 py-1 text-muted-foreground text-sm">
              {loading ? 'Ładowanie...' : 'Brak dostępnych działów'}
            </div>
          ) : (
            divisions.map((d) => (
              <SelectItem key={d.id} value={d.value}>
                {d.value}
              </SelectItem>
            ))
          )}
        </SelectGroup>
      </SelectContent>
    </Select>
  );
}

export default SelectDivision;
