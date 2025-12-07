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

function SelectReservationVariantPayment({ name }: Props) {
  const [field, meta, helpers] = useField<string>(name);

  return (
    <Select
      value={field.value || ''}
      onValueChange={(newValue) => helpers.setValue(newValue)}
    >
      <SelectTrigger className="w-full">
        <SelectValue placeholder="user" />
      </SelectTrigger>

      <SelectContent>
        <SelectGroup>
          <SelectLabel></SelectLabel>

          <SelectItem value="admin">admin</SelectItem>
          <SelectItem value="user">user</SelectItem>
        </SelectGroup>
      </SelectContent>
    </Select>
  );
}

export default SelectReservationVariantPayment;
