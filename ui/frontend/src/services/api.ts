import type {
  EmaAuthorizedProductGroup,
  EmaAuthorizedProduct,
  EmaProductFilters,
  MarketAuthorization,
  PaginatedResponse
} from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || '/api';

interface SortParams {
  field: string;
  order: 'ascend' | 'descend';
}

/**
 * Fetch paginated EMA authorized product groups with optional filters, search, and sorting
 */
export async function fetchEmaProducts(
  page: number,
  pageSize: number,
  filters?: EmaProductFilters,
  search?: string,
  sorter?: SortParams
): Promise<PaginatedResponse<EmaAuthorizedProductGroup>> {
  const params = new URLSearchParams({
    page: (page - 1).toString(),
    size: pageSize.toString()
  });

  // Add filter parameters
  if (filters?.status && filters.status.length > 0) {
    filters.status.forEach((value) => params.append('status', String(value)));
  }
  if (
    filters?.authorization_holder_country &&
    filters.authorization_holder_country.length > 0
  ) {
    filters.authorization_holder_country.forEach((value) =>
      params.append('authorization_holder_country', String(value))
    );
  }
  if (filters?.therapeutic_group && filters.therapeutic_group.length > 0) {
    filters.therapeutic_group.forEach((value) =>
      params.append('therapeutic_group', String(value))
    );
  }

  // Add search parameter
  if (search && search.trim()) {
    params.append('search', search.trim());
  }

  // Add sort parameters
  if (sorter && sorter.field && sorter.order) {
    params.append(
      'sort',
      `${sorter.field},${sorter.order === 'ascend' ? 'asc' : 'desc'}`
    );
  }

  const response = await fetch(
    `${API_BASE_URL}/ema-authorized-product-groups?${params.toString()}`
  );

  if (!response.ok) {
    throw new Error(`Failed to fetch products: ${response.statusText}`);
  }

  return response.json();
}

/**
 * Fetch products for a specific product group
 */
export async function fetchProductsByGroupId(
  groupId: number | string
): Promise<EmaAuthorizedProduct[]> {
  const params = new URLSearchParams({
    emaProductNumber: String(groupId)
  });

  const response = await fetch(
    `${API_BASE_URL}/ema-authorized-product-groups/products?${params.toString()}`
  );

  if (!response.ok) {
    throw new Error(`Failed to fetch products: ${response.statusText}`);
  }

  return response.json();
}

/**
 * Fetch market authorizations for a specific product number
 */
export async function fetchMarketAuthorizations(
  productNumber: string
): Promise<MarketAuthorization[]> {
  const params = new URLSearchParams({
    productNumber: String(productNumber)
  });

  const response = await fetch(
    `${API_BASE_URL}/ema-authorized-products/market_authorizations?${params.toString()}`
  );

  if (!response.ok) {
    throw new Error(`Failed to fetch market authorizations: ${response.statusText}`);
  }

  return response.json();
}

/**
 * Fetch source item details for a specific source and product number
 */
export async function fetchSourceItem(
  source: string,
  productNumber: string
): Promise<Record<string, unknown>> {
  const params = new URLSearchParams({
    productNumber: String(productNumber)
  });

  const response = await fetch(
    `${API_BASE_URL}/ema-authorized-products/market_authorizations/${source}?${params.toString()}`
  );

  if (!response.ok) {
    throw new Error(`Failed to fetch source item: ${response.statusText}`);
  }

  return response.json();
}
