<?php
 return [
  'name' => 'tenancy',
  'label' => 'Wohnen',
  'info' => '',
  'type' => 'collection',
  'fields' => [
    0 => [
      'name' => 'housing',
      'type' => 'contentItemLink',
      'label' => 'Unterkunft',
      'info' => '',
      'group' => '',
      'i18n' => false,
      'required' => false,
      'multiple' => false,
      'meta' => [
      ],
      'opts' => [
        'link' => 'housing',
        'filter' => NULL,
      ],
    ],
    1 => [
      'name' => 'person',
      'type' => 'contentItemLink',
      'label' => 'Person',
      'info' => '',
      'group' => '',
      'i18n' => false,
      'required' => false,
      'multiple' => false,
      'meta' => [
      ],
      'opts' => [
        'link' => 'person',
        'filter' => NULL,
      ],
    ],
    2 => [
      'name' => 'startDate',
      'type' => 'date',
      'label' => 'Einzug',
      'info' => '',
      'group' => '',
      'i18n' => false,
      'required' => false,
      'multiple' => false,
      'meta' => [
      ],
      'opts' => [
      ],
    ],
    3 => [
      'name' => 'EndDate',
      'type' => 'date',
      'label' => 'Auszug',
      'info' => '',
      'group' => '',
      'i18n' => false,
      'required' => false,
      'multiple' => false,
      'meta' => [
      ],
      'opts' => [
      ],
    ],
  ],
  'preview' => [
  ],
  'group' => 'Wohnen',
  'meta' => NULL,
  '_created' => 1764890641,
  '_modified' => 1764890641,
  'color' => NULL,
  'revisions' => false,
];