import { useEffect, useState } from 'react';
import * as yup from 'yup';
import { Formik, Field, Form } from 'formik';
import { Button } from '@/components/ui/button';
import { Label } from '@/components/ui/label';
import { Input } from '@/components/ui/input';
import SelectReservationVariantPayment from '../SelectUserType';
import SelectDepartment from '../SelectDep';

import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';

type User = {
  id: number;
  username: string;
  name: string;
  surname: string;
  department: string;
  user_type: string;
};

function MangeUser() {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null); // błąd listy
  const [submitError, setSubmitError] = useState<string | null>(null); // błąd dodawania

  const validationSchema = yup.object({
    userName: yup
      .string()
      .trim()
      .required('Podaj nazwę użytkownika')
      .min(3, 'Nazwa użytkownika musi mieć przynajmniej 3 znaki')
      .max(40, 'Nazwa użytkownika może mieć maksymalnie 40 znaków'),
    name: yup
      .string()
      .trim()
      .required('Podaj imię użytkownika')
      .min(3, 'Imię użytkownika musi mieć przynajmniej 3 znaki')
      .max(40, 'Imię użytkownika może mieć maksymalnie 15 znaków'),
    password: yup
      .string()
      .required('Hasło jest wymagane')
      .min(8, 'Hasło musi mieć min. 8 znaków')
      .matches(/[A-Z]/, 'Hasło musi posiadac przynajmniej jedną wielką literę')
      .matches(/[a-z]/, 'Hasło musi posiadac przynajmniej jedną mała literę')
      .matches(/\d/, 'Hasło musi posiadac przynajmniej jedną cyfrę')
      .matches(
        /[!@#$%^&*(),.?":{}|<>]/,
        'Hasło musi posiadac przynajmniej jeden znak specjalny'
      ),
    surname: yup
      .string()
      .trim()
      .required('Podaj nazwisko użytkownika')
      .min(3, 'Nazwisko użytkownika musi mieć przynajmniej 3 znaki')
      .max(40, 'Nazwisko użytkownika może mieć maksymalnie 15 znaków'),
    department: yup.string().required('Wybierz dział'),
    user_type: yup
      .string()
      .oneOf(['admin', 'user'], 'Wybierz admin lub user')
      .required('Wybierz typ użytkownika'),
  });

  // pobranie użytkowników z backendu
  useEffect(() => {
    const fetchUsers = async () => {
      setLoading(true);
      setError(null);
      try {
        const res = await fetch('/api/user/all-users');
        if (!res.ok) {
          throw new Error(`HTTP error! status: ${res.status}`);
        }
        const data = (await res.json()) as User[];
        setUsers(data);
      } catch (err) {
        console.error('Error fetching users:', err);
        setError('Nie udało się pobrać listy użytkowników.');
      } finally {
        setLoading(false);
      }
    };

    fetchUsers();
  }, []);

  return (
    <div className="flex flex-col items-center gap-6">
      {/* FORMULARZ DODAWANIA UŻYTKOWNIKA */}
      <div
        className="container flex flex-col items-center w-[80vw] h-[42vh] gap-[2vh] border-2 rounded-lg p-6"
        style={{
          borderColor: 'var(--primary)',
        }}
      >
        <h2 className="text-xl font-bold">Dodaj nowego użytkownika</h2>
        <Formik
          enableReinitialize
          validationSchema={validationSchema}
          initialValues={{
            userName: '',
            name: '',
            surname: '',
            password: '',
            department: '',
            user_type: '',
          }}
          validateOnChange={false}
          onSubmit={async (values, { resetForm }) => {
            try {
              setSubmitError(null);

              const payload = {
                username: values.userName,
                name: values.name,
                surname: values.surname,
                password: values.password,
                department: values.department,
                user_type: values.user_type,
              };

              const res = await fetch('/api/user/register', {
                method: 'POST',
                headers: {
                  'Content-Type': 'application/json',
                },
                body: JSON.stringify(payload),
              });

              if (!res.ok) {
                throw new Error(`HTTP error! status: ${res.status}`);
              }

              const createdUser = (await res.json()) as User;

              // dopisz nowego użytkownika do istniejącej listy
              setUsers((prev) => [...prev, createdUser]);

              resetForm();
            } catch (err) {
              console.error('Error registering user:', err);
              setSubmitError('Nie udało się dodać użytkownika.');
            }
          }}
        >
          {() => (
            <div className="container flex flex-col items-center w-[80vw] gap-[2vh]">
              <Form>
                <div className="grid grid-cols-3 grid-rows-2 gap-[1vw] h-[25vh] w-[65vw]">
                  {/* Nazwa użytkownika */}
                  <div className="grid gap-3 ">
                    <Field name="userName">
                      {({ field, meta }: any) => (
                        <div className="grid gap-2">
                          <Label htmlFor="userName">Nazwa użytkownika</Label>
                          <Input
                            id="userName"
                            type="text"
                            placeholder="jan.kowalski"
                            {...field}
                            onKeyDown={(e) => {
                              if (e.key === 'Enter')
                                (e.target as HTMLInputElement).blur();
                            }}
                          />
                          <p
                            className={`text-xs text-center ${
                              meta.touched && meta.error
                                ? 'text-red-500'
                                : 'invisible'
                            }`}
                            aria-live="polite"
                            id="userName-error"
                          >
                            {meta.error || 'placeholder'}
                          </p>
                        </div>
                      )}
                    </Field>
                  </div>

                  {/* Imię */}
                  <div className="grid gap-3 ">
                    <Field name="name">
                      {({ field, meta }: any) => (
                        <div className="grid gap-2">
                          <Label htmlFor="name">Imię</Label>
                          <Input
                            id="name"
                            type="text"
                            placeholder="Jan"
                            {...field}
                            onKeyDown={(e) => {
                              if (e.key === 'Enter')
                                (e.target as HTMLInputElement).blur();
                            }}
                          />
                          <p
                            className={`text-xs text-center ${
                              meta.touched && meta.error
                                ? 'text-red-500'
                                : 'invisible'
                            }`}
                            aria-live="polite"
                            id="name-error"
                          >
                            {meta.error || 'placeholder'}
                          </p>
                        </div>
                      )}
                    </Field>
                  </div>

                  {/* Nazwisko */}
                  <div className="grid gap-3 ">
                    <Field name="surname">
                      {({ field, meta }: any) => (
                        <div className="grid gap-2">
                          <Label htmlFor="surname">Nazwisko</Label>
                          <Input
                            id="surname"
                            type="text"
                            placeholder="Kowalski"
                            {...field}
                            onKeyDown={(e) => {
                              if (e.key === 'Enter')
                                (e.target as HTMLInputElement).blur();
                            }}
                          />
                          <p
                            className={`text-xs text-center ${
                              meta.touched && meta.error
                                ? 'text-red-500'
                                : 'invisible'
                            }`}
                            aria-live="polite"
                            id="surname-error"
                          >
                            {meta.error || 'placeholder'}
                          </p>
                        </div>
                      )}
                    </Field>
                  </div>

                  {/* Hasło */}
                  <div className="grid gap-3">
                    <Field name="password">
                      {({ field, meta }: any) => (
                        <div className="grid gap-2">
                          <Label htmlFor="password">Podaj hasło</Label>
                          <Input
                            id="password"
                            type="password"
                            {...field}
                            onKeyDown={(e) => {
                              if (e.key === 'Enter')
                                (e.target as HTMLInputElement).blur();
                            }}
                          />
                          <p
                            className={`text-xs text-center ${
                              meta.touched && meta.error
                                ? 'text-red-500'
                                : 'invisible'
                            }`}
                            aria-live="polite"
                            id="password-error"
                          >
                            {meta.error || 'placeholder'}
                          </p>
                        </div>
                      )}
                    </Field>
                  </div>

                  {/* Dział */}
                  <div className="grid gap-3 ">
                    <Field name="department">
                      {({ meta }: any) => (
                        <div className="grid gap-2">
                          <Label htmlFor="department">Dział</Label>
                          <SelectDepartment name="department" />
                          <p
                            className={`text-xs text-center ${
                              meta.touched && meta.error
                                ? 'text-red-500'
                                : 'invisible'
                            }`}
                            aria-live="polite"
                            id="department-error"
                          >
                            {meta.error || 'placeholder'}
                          </p>
                        </div>
                      )}
                    </Field>
                  </div>

                  {/* Typ użytkownika */}
                  <div className="grid gap-3 ">
                    <Field name="user_type">
                      {({ meta }: any) => (
                        <div className="grid gap-2">
                          <Label htmlFor="user_type">Typ użytkownika</Label>
                          <SelectReservationVariantPayment name="user_type" />
                          <p
                            className={`text-xs text-center ${
                              meta.touched && meta.error
                                ? 'text-red-500'
                                : 'invisible'
                            }`}
                            aria-live="polite"
                            id="user_type-error"
                          >
                            {meta.error || 'placeholder'}
                          </p>
                        </div>
                      )}
                    </Field>
                  </div>
                </div>

                <div className="pt-2">
                  <Button type="submit" className="w-full">
                    Dodaj użytkownika
                  </Button>
                  {submitError && (
                    <p className="mt-2 text-sm text-red-500 text-center">
                      {submitError}
                    </p>
                  )}
                </div>
              </Form>
            </div>
          )}
        </Formik>
      </div>

      {/* TABELA Z UŻYTKOWNIKAMI Z NOWEGO ENDPOINTU */}
      <div className="container flex flex-col w-[80vw] max-h-[45vh] rounded-lg p-4">
        <h2 className="text-xl font-bold mb-4">Lista użytkowników</h2>

        {loading && <p>Wczytywanie użytkowników...</p>}
        {error && (
          <p className="text-sm text-red-500 mb-2">
            {error}
          </p>
        )}

        {!loading && !error && users.length === 0 && (
          <p>Brak użytkowników do wyświetlenia.</p>
        )}

        {!loading && users.length > 0 && (
          <div className="overflow-x-auto overflow-y-auto max-h-[35vh]">
            <Table className="min-w-max w-full">
              <TableHeader className="bg-gray-100 sticky top-0 z-10">
                <TableRow>
                  <TableHead className="px-2 py-2 text-left font-bold border-x border-y">
                    ID
                  </TableHead>
                  <TableHead className="px-2 py-2 text-left font-bold border-x border-y">
                    Nazwa użytkownika
                  </TableHead>
                  <TableHead className="px-2 py-2 text-left font-bold border-x border-y">
                    Imię
                  </TableHead>
                  <TableHead className="px-2 py-2 text-left font-bold border-x border-y">
                    Nazwisko
                  </TableHead>
                  <TableHead className="px-2 py-2 text-left font-bold border-x border-y">
                    Dział
                  </TableHead>
                  <TableHead className="px-2 py-2 text-left font-bold border-x border-y">
                    Typ użytkownika
                  </TableHead>
                </TableRow>
              </TableHeader>

              <TableBody>
                {users.map((user) => (
                  <TableRow key={user.id} className="hover:bg-gray-50">
                    <TableCell className="px-2 py-2 text-left border-x border-y">
                      {user.id}
                    </TableCell>
                    <TableCell className="px-2 py-2 text-left border-x border-y">
                      {user.username}
                    </TableCell>
                    <TableCell className="px-2 py-2 text-left border-x border-y">
                      {user.name}
                    </TableCell>
                    <TableCell className="px-2 py-2 text-left border-x border-y">
                      {user.surname}
                    </TableCell>
                    <TableCell className="px-2 py-2 text-left border-x border-y">
                      {user.department}
                    </TableCell>
                    <TableCell className="px-2 py-2 text-left border-x border-y">
                      {user.user_type}
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>
        )}
      </div>
    </div>
  );
}

export default MangeUser;
