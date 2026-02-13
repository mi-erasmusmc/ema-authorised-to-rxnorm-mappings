export interface ActiveSubstanceDto {
  concept_id: number | null;
  concept_name: string;
}

export interface BrandDto {
  concept_id: number | null;
  concept_name: string;
}

export interface SupplierDto {
  concept_id: number | null;
  concept_name: string;
}

export interface EmaAuthorizedProductGroup {
  id: string;
  product_number: string;
  group_auth_number: string;
  name: string;
  authorization_holder: string;
  authorization_holder_country: string;
  status: string;
  atc_code: string;
  therapeutic_group: string;
  authorisation_date: string;
  refusal_date?: string;
  suspension_date?: string;
  medicine_url: string;
  therapeutic_indication: string;
  standardized_ingredients: ActiveSubstanceDto[];
  standardized_brands: BrandDto[];
  standardized_suppliers: SupplierDto[];
  active_substance_count: number;
}

export interface EmaAuthorizedProduct {
  id: string;
  product_auth_number: string;
  ma_number: string;
  name: string;
  authorisation_holder: string;
  strength: string | null;
  pharmaceutical_form: string | null;
  route_of_administration: string | null;
  packaging: string | null;
  content: string | null;
  pack_size: string | null;
  country_codes: string[];
  concept_id: number | null;
  concept_name: string | null;
}

export interface MarketAuthorization {
  ma_number: string;
  items: SourceItemInfo[];
}

export interface SourceItemInfo {
  source: string;
  source_code: string;
}

export interface PaginatedResponse<T> {
  content: T[];
  number: number;
  size: number;
  total_elements: number;
  total_pages: number;
}

export interface EmaProductFilters {
  status?: string[];
  authorization_holder_country?: string[];
  therapeutic_group?: string[];
}
