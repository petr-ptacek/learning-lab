import { PageLayout } from "./PageLayout.tsx";
import { Alert }      from "./Alert.tsx";

export default function App() {
  const header = (
    <div>Header</div>
  );

  const footer = (
    <div>Footer</div>
  );


  return (
    <div>
      <PageLayout header={ header } footer={ footer }>
        <Alert icon="✅"> Uloženo.</Alert>
      </PageLayout>

      <PageLayout header={ header } footer={ footer }>
        <p>Lorem ipsum dolor sit amet, consectetur adipisicing elit. Facilis, tempora?</p>
        <p>Lorem ipsum dolor sit amet, consectetur adipisicing elit. Facilis, tempora?</p>
      </PageLayout>

      <PageLayout header="Header Slot" footer={ 124 }>
        <p>Lorem ipsum dolor sit amet, consectetur adipisicing elit. Facilis, tempora?</p>
      </PageLayout>
    </div>
  );
}