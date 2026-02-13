interface ConceptLinkProps {
  conceptId: number | null;
  conceptName: string | null;
  showId?: boolean;
  showName?: boolean;
}

function ConceptLink({
  conceptId,
  conceptName,
  showId = true,
  showName = true
}: ConceptLinkProps) {
  if (!conceptId && !conceptName) {
    return <span style={{ color: '#999' }}>Not mapped</span>;
  }

  const athenaUrl = conceptId
    ? `https://athena.ohdsi.org/search-terms/terms/${conceptId}`
    : null;

  const displayText = [
    showId && conceptId ? conceptId : null,
    showName && conceptName ? conceptName : null
  ]
    .filter(Boolean)
    .join(' - ');

  if (athenaUrl) {
    return (
      <a
        href={athenaUrl}
        target="_blank"
        rel="noopener noreferrer"
        style={{ color: '#01452c' }}
      >
        {displayText}
      </a>
    );
  }

  return <span>{displayText}</span>;
}

export default ConceptLink;
