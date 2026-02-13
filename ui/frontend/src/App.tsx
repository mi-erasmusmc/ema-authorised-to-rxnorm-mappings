import { ConfigProvider, Layout } from 'antd';
import Art57Header from './components/Header';
import EmaProductsTable from './components/EmaProductsTable';

const { Content } = Layout;

function App() {
  return (
    <ConfigProvider
      theme={{
        token: {
          colorPrimary: '#01452c',
          colorLink: '#01452c',
          colorLinkHover: '#026638',
          colorLinkActive: '#013320',
        },
      }}
    >
      <Layout style={{ minHeight: '100vh' }}>
        <Art57Header />
        <Content style={{ backgroundColor: '#F3F7FC' }}>
          <EmaProductsTable />
        </Content>
      </Layout>
    </ConfigProvider>
  );
}

export default App;
