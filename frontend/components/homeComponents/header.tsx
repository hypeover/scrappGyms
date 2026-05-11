"use client";
import NumberFlow from "@number-flow/react";
import { useEffect, useState } from "react";

const LenHeader = ({ dataLen }: { dataLen: number }) => {
  const [value, setValue] = useState(0);

  useEffect(() => {
    setValue(dataLen);
  }, []);

  return (
    <h1 className="font-semibold my-5 text-3xl font-mono">
      Aktualnie na mapie jest <NumberFlow value={value} /> obiektów.
    </h1>
  );
};

export default LenHeader;
