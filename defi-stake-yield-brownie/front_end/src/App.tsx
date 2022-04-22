import React from "react";
import { ChainId, DAppProvider } from "@usedapp/core";
import { Header } from "./components/Header";
import { Container } from "@material-ui/core";

function App() {
  return (
    <DAppProvider
      config={{
        supportedChains: [ChainId.Kovan, ChainId.Rinkeby, 1337],
      }}
    >
      <Header />
      <Container>
        <div>Hi!</div>
      </Container>
    </DAppProvider>
  );
}

export default App;
