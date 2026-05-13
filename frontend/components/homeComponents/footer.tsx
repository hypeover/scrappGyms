import React from "react";

const Footer = () => {
  const data = [
    { network: "JustGym,", link: "https://justgym.pl/" },
    { network: "Zdrofit,", link: "https://zdrofit.pl/" },
    { network: "Fitness Academy,", link: "https://fitness-academy.com.pl/" },
    { network: "Fabryka Formy,", link: "https://fabryka-formy.pl/" },
    { network: "Calypso,", link: "https://www.calypso.com.pl/" },
    { network: "CityFit,", link: "https://cityfit.pl/" },
    { network: "FitFabric,", link: "https://fitfabric.pl/" },
    { network: "Xtreme Fitness,", link: "https://www.xtremefitness.pl/" },
    { network: "WellFitness.", link: "https://wellfitness.pl/" },
  ];

  return (
    <div style={{fontSize: '12px'}} className="text-ring mb-5">
      Dane o lokalizacjach i godzinach otwarcia obiektów fitness pochodzą z
      publicznie dostępnych stron internetowych sieci: {data.map((gym, key) => (
        <a target="_blank" key={key} className="font-semibold text-black-600" href={gym.link}>{gym.network} </a>
      ))}Projekt ma charakter wyłącznie
      informacyjny i edukacyjny. Wszelkie nazwy marek, logotypy oraz znaki
      towarowe należą do ich prawnych właścicieli i zostały użyte jedynie w celu
      identyfikacji obiektów. Autor nie rości sobie żadnych praw autorskich do
      tych danych i nie gwarantuje ich 100% aktualności (zawsze zalecamy
      sprawdzenie informacji bezpośrednio u źródła).
    </div>
  );
};

export default Footer;
