import { useCallback, useEffect, useState } from 'react';
import { Button, Input, Table, TableProps, Spin } from 'antd';
import type { ColumnsType, TablePaginationConfig } from 'antd/es/table';
import ConceptLink from './ConceptLink';
import * as api from '../services/api';
import type {
  EmaAuthorizedProductGroup,
  EmaAuthorizedProduct,
  EmaProductFilters,
  ActiveSubstanceDto,
  BrandDto,
  SupplierDto
} from '../types';

type OnChange = NonNullable<TableProps<EmaAuthorizedProductGroup>['onChange']>;
type Filters = Parameters<OnChange>[1];

function EmaProductsTable() {
  const [data, setData] = useState<EmaAuthorizedProductGroup[]>([]);
  const [loading, setLoading] = useState(true);
  const [pagination, setPagination] = useState<TablePaginationConfig>({
    current: 1,
    pageSize: 20,
    total: 0,
    showQuickJumper: true
  });
  const [filteredInfo, setFilteredInfo] = useState<Filters>({});
  const [searchTerm, setSearchTerm] = useState('');
  const [expandedRowKeys, setExpandedRowKeys] = useState<string[]>([]);
  const [expandedRowProducts, setExpandedRowProducts] = useState<
    Record<string, EmaAuthorizedProduct[]>
  >({});
  const [expandedRowLoading, setExpandedRowLoading] = useState<
    Record<string, boolean>
  >({});


  const fetchEmaProducts = useCallback(
    (
      page: number,
      pageSize: number,
      filters?: Filters,
      search?: string,
      sorter?: { field: string; order: 'ascend' | 'descend' }
    ) => {
      setLoading(true);

      const emaProductFilters: EmaProductFilters = {
        status: filters?.status as string[] | undefined,
        authorization_holder_country: filters?.authorization_holder_country as
          | string[]
          | undefined,
        therapeutic_group: filters?.therapeutic_group as string[] | undefined
      };

      api
        .fetchEmaProducts(page, pageSize, emaProductFilters, search, sorter)
        .then((response) => {
          setData(response.content);
          setPagination({
            current: response.number + 1,
            pageSize: response.size,
            total: response.total_elements,
            showQuickJumper: true
          });
          setLoading(false);
        })
        .catch((error) => {
          console.error('Error loading EMA products:', error);
          setLoading(false);
        });
    },
    []
  );

  useEffect(() => {
    fetchEmaProducts(1, 20);
  }, [fetchEmaProducts]);

  const handleTableChange: OnChange = useCallback(
    (newPagination, filters, sorter) => {
      setFilteredInfo(filters);

      // Extract sorter info if it's not an array
      let sorterInfo:
        | { field: string; order: 'ascend' | 'descend' }
        | undefined;
      if (!Array.isArray(sorter) && sorter.field && sorter.order) {
        sorterInfo = {
          field: sorter.field as string,
          order: sorter.order
        };
      }

      fetchEmaProducts(
        newPagination.current || 1,
        newPagination.pageSize || 20,
        filters,
        searchTerm,
        sorterInfo
      );
    },
    [searchTerm, fetchEmaProducts]
  );

  const clearFilters = useCallback(() => {
    setFilteredInfo({});
    setSearchTerm('');
    fetchEmaProducts(1, 20, {}, '');
  }, [fetchEmaProducts]);

  const handleSearch = useCallback(() => {
    fetchEmaProducts(1, 20, filteredInfo, searchTerm, undefined);
  }, [filteredInfo, searchTerm, fetchEmaProducts]);

  const handleExpand = useCallback(
    (expanded: boolean, record: EmaAuthorizedProductGroup) => {
      if (expanded) {
        setExpandedRowKeys([...expandedRowKeys, record.id]);

        // Only fetch if we don't have the data already
        if (!expandedRowProducts[record.id]) {
          setExpandedRowLoading({ ...expandedRowLoading, [record.id]: true });

          api
            .fetchProductsByGroupId(record.id)
            .then((products) => {
              setExpandedRowProducts({
                ...expandedRowProducts,
                [record.id]: products
              });
              setExpandedRowLoading({
                ...expandedRowLoading,
                [record.id]: false
              });
            })
            .catch((error) => {
              console.error('Error loading products:', error);
              setExpandedRowLoading({
                ...expandedRowLoading,
                [record.id]: false
              });
            });
        }
      } else {
        setExpandedRowKeys(expandedRowKeys.filter((key) => key !== record.id));
      }
    },
    [expandedRowKeys, expandedRowProducts, expandedRowLoading]
  );


  const expandedRowRender = useCallback(
    (record: EmaAuthorizedProductGroup) => {
      const loading = expandedRowLoading[record.id];
      const products = expandedRowProducts[record.id] || [];

      if (loading) {
        return (
          <div style={{ textAlign: 'center', padding: '20px' }}>
            <Spin />
          </div>
        );
      }

      if (products.length === 0) {
        return (
          <div style={{ padding: '20px', color: '#999' }}>
            No products found for this group
          </div>
        );
      }

      const productColumns: ColumnsType<EmaAuthorizedProduct> = [
        {
          title: 'Authorization Number',
          dataIndex: 'ma_number',
          key: 'ma_number',
          width: 200,
          render: (value: string) => value || 'N/A'
        },
        {
          title: 'Concept',
          key: 'concept',
          width: 250,
          render: (_value: unknown, record: EmaAuthorizedProduct) => {
            if (record.concept_id && record.concept_name) {
              return (
                <ConceptLink
                  conceptId={record.concept_id}
                  conceptName={record.concept_name}
                  showId={false}
                  showName={true}
                />
              );
            }
            return <span style={{ color: '#999' }}>Not mapped</span>;
          }
        },
        {
          title: 'Strength',
          dataIndex: 'strength',
          key: 'strength',
          width: 150,
          render: (value: string) => value || 'N/A'
        },
        {
          title: 'Content',
          dataIndex: 'content',
          key: 'content',
          width: 200,
          render: (value: string) => value || 'N/A'
        },
        {
          title: 'Route of Administration',
          dataIndex: 'route_of_administration',
          key: 'route_of_administration',
          width: 200,
          render: (value: string) => value || 'N/A'
        },
        {
          title: 'Pharmaceutical Form',
          dataIndex: 'pharmaceutical_form',
          key: 'pharmaceutical_form',
          width: 200,
          render: (value: string) => value || 'N/A'
        },
        {
          title: 'Pack Size',
          dataIndex: 'pack_size',
          key: 'pack_size',
          width: 150,
          render: (value: string) => value || 'N/A'
        },
        {
          title: 'Packaging',
          dataIndex: 'packaging',
          key: 'packaging',
          width: 200,
          render: (value: string) => value || 'N/A'
        }
      ];

      return (
        <div style={{ padding: '0 20px 20px 20px' }}>
          <Table
            columns={productColumns}
            dataSource={products}
            rowKey="id"
            pagination={false}
            size="small"
            bordered
          />
        </div>
      );
    },
    [expandedRowLoading, expandedRowProducts]
  );

  const columns: ColumnsType<EmaAuthorizedProductGroup> = [
    {
      title: 'product number',
      dataIndex: 'medicine_url',
      key: 'medicine_url',
      width: 150,
      align: 'center',
      render: (value: string, record: EmaAuthorizedProductGroup) => {
        if (!value) return 'N/A';
        return (
          <a
            href={value}
            target="_blank"
            rel="noopener noreferrer"
            style={{ color: '#01452c' }}
          >
            {record.product_number || 'Link'}
          </a>
        );
      }
    },
    {
      title: 'name',
      dataIndex: 'standardized_brands',
      key: 'standardized_brands',
      minWidth: 300,
      render: (brands: BrandDto[], record: EmaAuthorizedProductGroup) => {
        if (!brands || brands.length === 0) return 'N/A';
        return (
          <div>
            {brands.map((_brand, index) => (
              <div
                key={index}
                style={{
                  padding: '4px 0',
                  paddingBottom: index < brands.length - 1 ? '10px' : '0'
                }}
              >
                  <span>{record.name}</span>
              </div>
            ))}
          </div>
        );
      }
    },
    {
      title: 'active substances',
      dataIndex: 'standardized_ingredients',
      key: 'standardized_ingredients',
      minWidth: 250,
      render: (substances: ActiveSubstanceDto[]) => {
        if (!substances || substances.length === 0) return 'N/A';
        return (
          <div>
            {substances.map((substance, index) => (
              <div
                key={index}
                style={{
                  padding: '4px 0',
                  paddingBottom: index < substances.length - 1 ? '10px' : '0'
                }}
              >
                {substance.concept_id ? (
                  <ConceptLink
                    conceptId={substance.concept_id}
                    conceptName={substance.concept_name}
                    showId={false}
                    showName={true}
                  />
                ) : (
                  <span>{substance.concept_name}</span>
                )}
              </div>
            ))}
          </div>
        );
      }
    },
    {
      title: 'authorization holder',
      dataIndex: 'standardized_suppliers',
      key: 'standardized_suppliers',
      width: 200,
      render: (suppliers: SupplierDto[], record: EmaAuthorizedProductGroup) => {
        if (!suppliers || suppliers.length === 0) return 'N/A';
        return (
          <div>
            {suppliers.map((supplier, index) => (
              <div
                key={index}
                style={{
                  padding: '4px 0',
                  paddingBottom: index < suppliers.length - 1 ? '10px' : '0'
                }}
              >
                {supplier.concept_id ? (
                  <ConceptLink
                    conceptId={supplier.concept_id}
                    conceptName={supplier.concept_name}
                    showId={false}
                    showName={true}
                  />
                ) : (
                  <span>{record.authorization_holder}</span>
                )}
              </div>
            ))}
          </div>
        );
      }
    },
    {
      title: 'ATC',
      dataIndex: 'atc_code',
      key: 'atc_code',
      align: 'center',
      minWidth: 100,
      sorter: (a, b) => (a.atc_code || '').localeCompare(b.atc_code || ''),
      render: (value: string) => {
        if (!value) return 'N/A';
        return (
          <a
            href={`https://atcddd.fhi.no/atc_ddd_index/?code=${value}`}
            target="_blank"
            rel="noopener noreferrer"
            style={{ color: '#01452c' }}
          >
            {value}
          </a>
        );
      }
    }
  ];

  return (
    <div style={{
      padding: '2em 5%',
      fontSize: '8px'
    }}>
      <div
        style={{
          marginBottom: '24px',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center'
        }}
      >
        <h1
          style={{
            marginBottom: '0',
            fontSize: '28px',
            fontWeight: '600',
            color: '#01452c'
          }}
        >
        </h1>
      </div>

      <div
        style={{
          marginBottom: '24px',
          display: 'flex',
          gap: '12px',
          alignItems: 'flex-end'
        }}
      >
        <div style={{ flex: 1 }}>
          <Input
            placeholder="Search by product number, name, authorization holder, or ATC code..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            onPressEnter={handleSearch}
            size="large"
            style={{ borderRadius: '8px' }}
          />
        </div>
        <Button
          type="primary"
          size="large"
          onClick={handleSearch}
          style={{
            borderRadius: '8px',
            height: '40px',
            paddingLeft: '24px',
            paddingRight: '24px'
          }}
        >
          search
        </Button>
      </div>

      {(Object.values(filteredInfo).some(
        (filter) => filter && filter.length > 0
      ) ||
        searchTerm) && (
        <div
          style={{
            display: 'flex',
            justifyContent: 'flex-end',
            marginBottom: '20px'
          }}
        >
          <Button onClick={clearFilters}>clear all filters</Button>
        </div>
      )}

      <Table
        columns={columns}
        dataSource={data}
        loading={loading}
        onChange={handleTableChange}
        rowKey="id"
        pagination={pagination}
        scroll={{ x: 1000 }}
        size="small"
        expandable={{
          expandedRowRender,
          onExpand: handleExpand,
          expandedRowKeys
        }}
      />

    </div>
  );
}

export default EmaProductsTable;
