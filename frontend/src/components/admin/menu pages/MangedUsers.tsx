import { useEffect, useState } from 'react';
import * as yup from 'yup';
import { Formik, Field, Form } from 'formik';
import { Button } from '@/components/ui/button';
import { Label } from '@/components/ui/label';
import { Input } from '@/components/ui/input';

function MangeUser() {
  return (
    <div>
      <div className="container flex flex-col items-center w-[80vw] gap-[2vh]">
        <h2 className="text-xl font-bold"> Dodaj nowego użytkonika</h2>
        <Formik
          enableReinitialize
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
                <div className="grid grid-cols-3 grid-rows-3 gap-[1vw] h-full w-[65vw]">
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
                          <Label htmlFor="user_type_id">Ttyp użytkownika</Label>
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
              </Form>
            </div>
          )}
        </Formik>
      </div>
    </div>
  );
}

export default MangeUser;
