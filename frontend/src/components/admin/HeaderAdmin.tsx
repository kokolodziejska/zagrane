function HeaderAdmin() {
  return (
    <div
      className="w-full flex flex-col"
      style={{
        height: 'var(--heder-height)',
        gap: 'var(--heder-gap-height)',
      }}
    >
      <div
        className="w-full flex flex-row items-center gap-x-6"
        style={{
          backgroundColor: 'var(--primary)',
          height: 'var(--heder-height-main)',
        }}
      >
        <div className="pl-[2vw]">
          <img
            src="/logo-biale.png"
            alt="Image"
            className="absolute top-[1vh] left-[2vh] h-[7vh] w-auto dark:brightness-[0.2] dark:grayscale"
          />
        </div>
      </div>
      <div
        className="animated-box w-full"
        style={{
          backgroundColor: 'var(--primary)',
          height: 'var(--heder-height-line)',
        }}
      ></div>
    </div>
  );
}

export default HeaderAdmin;
