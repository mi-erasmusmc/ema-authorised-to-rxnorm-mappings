import { useState } from 'react';
import { Header } from 'antd/es/layout/layout';
import { Drawer, Menu, MenuProps, Modal } from 'antd';
import {
  InfoCircleOutlined,
  MedicineBoxOutlined,
  MenuOutlined,
  UnorderedListOutlined,
} from '@ant-design/icons';
import hecateLogo from '../assets/hecate-logo.png';
import pantheonLogo from '../assets/pantheon.svg';

const headerStyle: React.CSSProperties = {
  height: 64,
  padding: 0,
  backgroundImage: 'linear-gradient(to left, white 16%, #01452c 84%)',
};

function Art57Header() {
  const [modalOpen, setModalOpen] = useState<boolean>(false);
  const [drawerOpen, setDrawerOpen] = useState<boolean>(false);

  const items: MenuProps['items'] = [
    {
      key: '1',
      label: (
        <div
          style={{
            fontSize: 'large',
            fontFamily: 'GFS Neohellenic',
            color: '#01452c',
          }}
        >
          Datasets
        </div>
      ),
      icon: (
        <UnorderedListOutlined
          style={{ fontSize: 'large', color: '#01452c' }}
        />
      ),
      children: [
        {
          key: '1-1',
          label: (
            <div
              onClick={() => setDrawerOpen(false)}
              style={{
                fontSize: 'large',
                fontFamily: 'GFS Neohellenic',
                color: '#01452c',
                cursor: 'pointer',
              }}
            >
              EMA Authorized Products
            </div>
          ),
          icon: (
            <MedicineBoxOutlined
              style={{ fontSize: 'large', color: '#01452c' }}
            />
          ),
        },
        {
          key: '1-2',
          label: (
            <div
              style={{
                fontSize: 'large',
                fontFamily: 'GFS Neohellenic',
                color: 'grey',
              }}
            >
              Additional datasets coming soon...
            </div>
          ),
          icon: (
            <MedicineBoxOutlined style={{ fontSize: 'large', color: 'grey' }} />
          ),
          disabled: true,
        },
      ],
    },
    {
      key: '2',
      label: (
        <div
          onClick={() => {
            setModalOpen(true);
            setDrawerOpen(false);
          }}
          style={{
            fontSize: 'large',
            fontFamily: 'GFS Neohellenic',
            color: '#01452c',
            cursor: 'pointer',
          }}
        >
          About
        </div>
      ),
      icon: (
        <InfoCircleOutlined style={{ fontSize: 'large', color: '#01452c' }} />
      ),
    },
  ];

  return (
    <Header style={headerStyle}>
      <div
        style={{
          display: 'flex',
          justifyContent: 'flex-end',
          height: '100%',
        }}
      >
        <div
          onClick={() => setDrawerOpen(true)}
          style={{
            marginRight: 'auto',
            paddingLeft: '1%',
            fontWeight: '500',
            fontSize: 38,
            fontFamily: 'GFS Neohellenic',
            color: '#F3F7FC',
            cursor: 'pointer',
          }}
        >
          <MenuOutlined style={{ marginRight: '0.5em', fontSize: '23px' }} />
          Art57
        </div>
        <img
          onClick={() => setModalOpen(true)}
          src={hecateLogo}
          alt="Hecate logo"
          style={{
            mixBlendMode: 'multiply',
            height: '100%',
            opacity: 0.8,
            paddingRight: '0.3em',
            cursor: 'pointer',
          }}
        />
      </div>

      <Drawer
        title="Menu"
        placement="left"
        onClose={() => setDrawerOpen(false)}
        open={drawerOpen}
        width="auto"
        styles={{
          header: {
            fontFamily: 'GFS Neohellenic',
            fontSize: 'large',
            color: '#01452c',
          },
          body: { padding: 0 },
        }}
      >
        <Menu
          mode="inline"
          items={items}
          style={{
            border: 'none',
            width: 'fit-content',
            minWidth: '250px',
            color: '#01452c',
          }}
        />
      </Drawer>

      <Modal
        style={{ fontFamily: 'GFS Neohellenic', color: '#01452c' }}
        title="About Art57"
        centered
        open={modalOpen}
        closable={true}
        footer={null}
        onCancel={() => setModalOpen(false)}
      >
        <div
          style={{
            display: 'flex',
            flexDirection: 'column',
            gap: '1em',
          }}
        >
          <div>
            Art57 provides a public interface to browse and search European Medicines Agency (EMA)
            authorized medicinal products mapped to RxNorm codes.
          </div>
          <div>
            Data is sourced from the{' '}
            <a
              href="https://github.com/mi-erasmusmc/ema-authorised-to-rxnorm-mappings"
              target="_blank"
              rel="noopener noreferrer"
              style={{ color: '#01452c' }}
            >
              ema-authorised-to-rxnorm-mappings
            </a>{' '}
            repository and is updated daily.
          </div>
          <div>
            Part of the Hecate Drug Mapper family of applications.
          </div>
          <div style={{ marginTop: '1em' }}>
            <img
              src={pantheonLogo}
              alt="Pantheon logo"
              style={{
                transform: 'scale(0.7)',
              }}
            />
            <div>info@pantheon-hds.com</div>
          </div>
        </div>
      </Modal>
    </Header>
  );
}

export default Art57Header;
