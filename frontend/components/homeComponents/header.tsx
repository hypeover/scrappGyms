"use client";
import NumberFlow from "@number-flow/react";
import { useEffect, useState } from "react";

const LenHeader = ({ dataLen }: { dataLen: number }) => {
  const [value, setValue] = useState(0);

  useEffect(() => {
    setValue(dataLen);
  }, []);

  return (
    <h1 className=" text-center font-semibold my-5 sm:text-2xl md:text-3xl text-md lg:text-3xl font-mono">
      Aktualnie na mapie jest <NumberFlow value={value} /> obiektów.
    </h1>
  );
};

export default LenHeader;
