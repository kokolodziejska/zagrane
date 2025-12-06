import { useEffect, useState } from 'react';
import * as yup from 'yup';
import { Formik, Field, Form } from 'formik';
import { Button } from '@/components/ui/button';
import { Label } from '@/components/ui/label';
import { Input } from '@/components/ui/input';

function MangeUser() {
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
    surname: yup
      .string()
      .trim()
      .required('Podaj nazwisko użytkownika')
      .min(3, 'Nazwisko użytkownika musi mieć przynajmniej 3 znaki')
      .max(40, 'Nazwisko użytkownika może mieć maksymalnie 15 znaków'),
    department_id: yup.string().trim().required('Podaj dział'),
    user_type_id: yup.string().trim().required('Podaj typ'),
  });

  return (
    <div>
      <div
        className="container flex flex-col items-center w-[80vw] h-[42vh] gap-[2vh] border-2 rounded-lg p-6"
        style={{
          borderColor: 'var(--primary)',
        }}
      >
        <h2 className="text-xl font-bold"> Dodaj nowego użytkonika</h2>
        <Formik
          enableReinitialize
          validationSchema={validationSchema}
          initialValues={{
            userName: '',
            name: '',
            surname: '',
            department_id: '',
            user_type_id: '',
          }}
          // validationSchema={validationSchema}
          validateOnChange={false}
          onSubmit={(values) => {}}
        >
          {({ resetForm }) => (
            <div className="container flex flex-col items-center w-[80vw] gap-[2vh]">
              <Form>
                <div className="grid grid-cols-3 grid-rows-2 gap-[1vw] h-[25vh] w-[65vw]">
                  <div className="grid gap-3 ">
                    <Field name="userName">
                      {({ field, meta }: any) => (
                        <div className="grid gap-2">
                          <Label htmlFor="userName">Nazwa użytkonika</Label>
                          <Input
                            id="userName"
                            type="string"
                            placeholder="jan.kowalski"
                            {...field}
                            onKeyDown={(e) => {
                              if (e.key === 'Enter') (e.target as HTMLInputElement).blur();
                            }}
                          />
                          <p
                            className={`text-xs text-center ${meta.touched && meta.error ? 'text-red-500' : 'invisible'}`}
                            aria-live="polite"
                            id="userName"
                          >
                            {meta.error || 'placeholder'}
                          </p>
                        </div>
                      )}
                    </Field>
                  </div>
                  <div className="grid gap-3 ">
                    <Field name="name">
                      {({ field, meta }: any) => (
                        <div className="grid gap-2">
                          <Label htmlFor="name">Imię</Label>
                          <Input
                            id="name"
                            type="string"
                            placeholder="Jan"
                            {...field}
                            onKeyDown={(e) => {
                              if (e.key === 'Enter') (e.target as HTMLInputElement).blur();
                            }}
                          />
                          <p
                            className={`text-xs text-center ${meta.touched && meta.error ? 'text-red-500' : 'invisible'}`}
                            aria-live="polite"
                            id="name"
                          >
                            {meta.error || 'placeholder'}
                          </p>
                        </div>
                      )}
                    </Field>
                  </div>
                  <div className="grid gap-3 ">
                    <Field name="surname">
                      {({ field, meta }: any) => (
                        <div className="grid gap-2">
                          <Label htmlFor="surname">Nazwisko</Label>
                          <Input
                            id="surname"
                            type="string"
                            placeholder="Kowalski"
                            {...field}
                            onKeyDown={(e) => {
                              if (e.key === 'Enter') (e.target as HTMLInputElement).blur();
                            }}
                          />
                          <p
                            className={`text-xs text-center ${meta.touched && meta.error ? 'text-red-500' : 'invisible'}`}
                            aria-live="polite"
                            id="surname"
                          >
                            {meta.error || 'placeholder'}
                          </p>
                        </div>
                      )}
                    </Field>
                  </div>
                  <div className="grid gap-3 ">
                    <Field name="department_id">
                      {({ field, meta }: any) => (
                        <div className="grid gap-2">
                          <Label htmlFor="department_id">Dział</Label>
                          <Input
                            id="department_id"
                            type="string"
                            placeholder="min cyf"
                            {...field}
                            onKeyDown={(e) => {
                              if (e.key === 'Enter') (e.target as HTMLInputElement).blur();
                            }}
                          />
                          <p
                            className={`text-xs text-center ${meta.touched && meta.error ? 'text-red-500' : 'invisible'}`}
                            aria-live="polite"
                            id="department_id"
                          >
                            {meta.error || 'placeholder'}
                          </p>
                        </div>
                      )}
                    </Field>
                  </div>
                  <div className="grid gap-3 ">
                    <Field name="user_type_id">
                      {({ field, meta }: any) => (
                        <div className="grid gap-2">
                          <Label htmlFor="user_type_id">Typ użytkownika</Label>
                          <Input
                            id="user_type_id"
                            type="string"
                            placeholder="admin"
                            {...field}
                            onKeyDown={(e) => {
                              if (e.key === 'Enter') (e.target as HTMLInputElement).blur();
                            }}
                          />
                          <p
                            className={`text-xs text-center ${meta.touched && meta.error ? 'text-red-500' : 'invisible'}`}
                            aria-live="polite"
                            id="user_type_id"
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
                    Dodaj użytkonika
                  </Button>
                  {/* <p
                    className={`text-xs text-center ${objectError ? 'text-red-500' : 'invisible'}`}
                    aria-live="polite"
                    id="submit"
                  >
                    {objectError || 'placeholder'}
                  </p> */}
                </div>
              </Form>
            </div>
          )}
        </Formik>
      </div>
    </div>
  );
}

export default MangeUser;
