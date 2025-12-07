import { useEffect, useState } from 'react';
import { useField } from 'formik';

import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectLabel,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';

type Props = { name: string };

function SelectDepartment({ name }: Props) {
  const [field, , helpers] = useField<string>(name);
  const [departments, setDepartments] = useState<string[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchDepartments = async () => {
      try {
        setLoading(true);
        setError(null);

        const res = await fetch('/api/departments/get_all_departments');
        if (!res.ok) {
          throw new Error(`HTTP error! status: ${res.status}`);
        }

        const data: string[] = await res.json(); // np. ["Department A", "Department B"]
        setDepartments(data);
      } catch (err) {
        console.error('Error fetching departments:', err);
        setError('Nie udało się pobrać listy działów');
      } finally {
        setLoading(false);
      }
    };

    fetchDepartments();
  }, []);

  return (
    <Select
      value={field.value || ''}
      onValueChange={(newValue) => helpers.setValue(newValue)}
    >
      <SelectTrigger className="w-full h-[40px] px-3">
        <SelectValue placeholder="Wybierz dział" />
      </SelectTrigger>

      <SelectContent>
        <SelectGroup>
          <SelectLabel>Dział</SelectLabel>

          {loading && (
            <SelectItem value="__loading" disabled>
              Ładowanie...
            </SelectItem>
          )}

          {error && !loading && (
            <SelectItem value="__error" disabled>
              {error}
            </SelectItem>
          )}

          {!loading &&
            !error &&
            departments.map((dep) => (
              <SelectItem key={dep} value={dep}>
                {dep}
              </SelectItem>
            ))}
        </SelectGroup>
      </SelectContent>
    </Select>
  );
}

export default SelectDepartment;
